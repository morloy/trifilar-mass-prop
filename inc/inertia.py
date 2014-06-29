"""All functions related to the moment of inertia and inertia tensor."""

from numpy import *
import os
import scipy.constants

import signal
import cog
import json

import constants as C
from tools import *

def PlotITest(I, Mt, R, name):
    """Create a plot for a inertia series measurements.
    The plot is written as a pdf file in the 'out' folder.

    Parameters
    ----------
    I : ndarray
        The inertia series
    Mt : float
        The test mass
    R : ndarray
        The measurements positions in m
    name : str
        Name for the measurement, appears in the title, may contain LaTeX.
    """
    X = linspace(R[0],R[-1], 20)
    It = lambda R: Mt * R**2

    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.tight_layout(pad=1.9)
    ax.plot(R, I*1000,'x', label=r"$I$")
    ax.plot(X, (It(X) + mean(I-It(R)))*1000, label=r'$I_t + \Delta I$')
    ax.set_xlabel(r'$r\,[m]$')
    ax.set_ylabel(r'$[g\,m^2]$')
    ax.set_title("${}$".format(name))
    ax.margins(.05)
    ax.legend(loc="best")
    Savefig(fig, name)

def GetInertiaSeries(workdir, name, M, Mt, R, p0):
    """Get the list of moments of inertia for a set of movies
    or .csv files given in the working directory.
    The movies/csv files have to be named after the position of the test mass
    in meters with a presicion of to, e.g. '0.3.csv' or '0.7.MP4'.

    Parameters
    ----------
    workdir : str
        The name of the working directoy
    name : str
        Name for the measurement, appears in the title, may contain LaTeX.
    M : float
        Mass of the system, e.g. unit mass + platform mass in kg.
    R : ndarray
        The measurements positions in m.
    p0 : array_like
        Initial parameters for the least-square fit

    Returns
    -------
    I : ndarray
        The inertia series.
    """
    I = []

    for r in R:
            filename = "{0}/{1}/{2:.2f}".format(workdir, name, r)
            T = signal.GetPeriod(filename, p0)
            I += [ C.R**2 / ( (2*pi)**2 * C.L) * scipy.constants.g * M * T**2 ]

    I = array(I)
    PlotITest(I, Mt, R, name)

    return array(I)

def GetISeries(workdir, name, M, Mt, R, p0, Ip):
    """Same as GetInertiaSeries(), but taking into account the
    platform inertia. Thus, gives the real unit moment of inertia.

    Parameters
    ----------
    workdir : str
        The name of the working directoy
    name : str
        Name of the measurement
    M : float
        Mass of the system, e.g. unit mass + platform mass in kg.
    R : ndarray
        The measurements positions in m.
    p0 : array_like
        Initial parameters for the least-square fit
    Ip : ndarray
        The platform inertia series, measured in the same positions and with the same test mass.

    Returns
    -------
    Iu : ndarray
        The bare unit inertia.
    """
    Iup = GetInertiaSeries(workdir, name, M, Mt, R, p0)
    Iu = Iup - Ip

    StatPrint("{}".format(name), Iu * 1000, "g m^2")

    return Iu

def GetDistanceFromAxis(p, axis):
    """Returns the distance of an arbitrary point from the given axis.

    Parameters
    ----------
    p : ndarray
        The point in 3D space.
    axis : str
        Identifier for the axis, must be one of 'xx', 'yy', 'zz', 'xy', 'xz', 'yz'.

    Returns:
    d : float
        The distance from the point to the axis.
    """
    N = {
                    'xx': [ 1., 0., 0. ],
                    'yy': [ 0., 1., 0. ],
                    'zz': [ 0., 0., 1. ],
                    'xy': ([ 1., 1., 0. ])/sqrt(2),
                    'xz': ([ 1., 0., 1. ])/sqrt(2),
                    'yz': ([ 0., 1., 1. ])/sqrt(2),
    }

    n = array(N[axis])
    d = norm(p - dot(p,n)*n)

    return d


def GetInertiaTensorSeries(workdir, Mu, Mp, Mt, R, p0, CoG3D):
    """Computes the series of the inertia tensor a given measurement series
    and a 3D center of gravity, taking into account the parallel axis theorem.

    Parameters
    ----------
    workdir : str
        The name of the working directoy
    Mu : float
        Unit mass
    Mu : float
        Platform mass
    Mu : float
        Test mass
    R : ndarray
        The measurements positions in m.
    p0 : array_like
        Initial parameters for the least-square fit
    CoG3D : ndarray
        The 3 coordinates of the center of gravity.

    Returns
    -------
    I : dict
        The inertia tensor as a dictionary containing entries 'xx', 'yy', etc.
        Each entry contains the series of results for the given component as an ndarray.
    """
    axes = ["xx", "yy", "zz", "xy", "xz", "yz"]

    Ip = GetInertiaSeries(workdir, "platform", Mp, Mt, R, p0)
    print "Platform:"
    StatPrint("I_p", Ip * 1000, "g m^2")
    print

    print "Moments of inertia:"
    ParAx = {}
    I = {}
    for ax in axes:
            # Apply parallel axis theorem
            d = GetDistanceFromAxis(CoG3D, ax)
            Ipa = Mu * d**2
            ParAx[ax] = [ d, Ipa ]

            I[ax] = GetISeries(workdir, ax, Mu + Mp, Mt, R, p0, Ip)# - Ipa
    print
    
    I['xy'] -= (I['xx'] + I['yy']) / 2.
    I['xz'] -= (I['xx'] + I['zz']) / 2.
    I['yz'] -= (I['yy'] + I['zz']) / 2.

    print "Parallel axis correction:"
    for ax in axes:
            print "{}: D = {} [mm], Ipa = {} [g m^2]".format(ax, ParAx[ax][0]*1000, ParAx[ax][1]*1000)
    print

    print "Tensor of Inertia:"
    for ax in axes:
            StatPrint("I_{{{}}}".format(ax), I[ax]*1000, "g m^2")

    return I
