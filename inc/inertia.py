from numpy import *
import os
import scipy.constants


import constants as C
import share as S
from tools import *
import signal
import cog
import json

from pprint import pprint

def PlotITest(I, Mt, R, name):
	X = linspace(R[0],R[-1], 20)
	It = lambda R: Mt * R**2

	fig = plt.figure()
	ax = fig.add_subplot(111)
	fig.tight_layout(pad=1.4)
	ax.plot(R, I*1000,'x', label=r"$I$")
	ax.plot(X, (It(X) + mean(I-It(R)))*1000, label=r'$I_t + \Delta I$')
	ax.set_xlabel(r'$r\,[m]$')
	ax.set_ylabel(r'$[g\,m^2]$')
	ax.set_title("${}$".format(name))
	ax.margins(.05)
	ax.legend(loc="best")
	Savefig(fig, name)

def GetInertiaSeries(workdir, name, M, Mt, R, p0):
	I = []

	for r in R:
		filename = "{0}/{1}/{2:.2f}".format(workdir, name, r)
		T = signal.GetPeriod(filename, p0)
		I += [ C.R**2 / ( (2*pi)**2 * C.L) * scipy.constants.g * M * T**2 ]

	I = array(I)
	PlotITest(I, Mt, R, name)

	return array(I)

def GetISeries(workdir, name, M, Mt, R, p0, Ip):
	Iup = GetInertiaSeries(workdir, name, M, Mt, R, p0)
	Iu = Iup - Ip

	StatPrint("{}".format(name), Iu * 1000, "g m^2")

	return Iu

def GetDistanceFromAxis(p, axis):
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
