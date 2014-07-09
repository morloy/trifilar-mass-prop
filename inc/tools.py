"""General tools"""

import constants as C

from numpy import *
from numpy.linalg import *
import scipy.constants

import os, sys, re
from os.path import splitext

from matplotlib import pyplot as plt

def pol2xy(r, theta):
	"""Converts polar coordinates from cartesian.

	Parameters
	----------
	r : float
		Radius
	theta : float
		Angle

	Returns
	-------
	ndarray
		x and y coordinates
	"""

	return array([ r*cos(theta), r*sin(theta) ])

def StatPrint(name, D, unit=''):
	"""Give information about a measurement series.

	Parameters
	----------
	name : str
		Name of measurements to format output.
	D : ndarray
		Data array
	unit : str
		Unit of the data
	"""
	global fig1, ax1, count, labels
	m = mean(D)
	s = std(D)
	perc = "({:.2f} %)".format(abs(s/m*100))
	if unit <> '':
		unit = '[{}]'.format(unit)
	print "{:<8} {:>17} {:>10} {:<10} {:<30}".format(name+':', un2str(m, s), perc, unit, D)

def Savefig(fig, name):
	"""Saves a figure in the 'out' directory, putting it in seperate a folder for each script.

	Parameters
	----------
	fig : Figure
		The figure object from matplotlib
	name : str
		Name of the figure, used for the output filename.
	"""
	out = "out"
	name_filtered = re.sub(r"[^A-Za-z0-9-]+", '', name.replace("'", "p"))
	script = splitext(sys.argv[0])[0]

	directory = "{}/{}".format(out, script)
	if not os.path.exists(directory):
		os.makedirs(directory)

	fig.savefig("{}/{}/{}.pdf".format(out, script, name_filtered))

from math import floor, log10

# uncertainty to string, adapted from
# http://stackoverflow.com/questions/6671053/python-pretty-print-errorbars
def un2str(x, xe, precision=2):
    """Pretty print nominal value and uncertainty

	Parameters
	----------
	x : float
		Nominal value
	xe : float
		Uncertainty
	precision : int
		Number of significant digits in uncertainty
	
	Returns
	-------
	str
		Shortest string representation of `x +- xe` either as
			x.xx(ee)e+xx
		or as
			xxx.xx(ee)
	"""
    # base 10 exponents
    x_exp = int(floor(log10(abs(x))))
    xe_exp = int(floor(log10(xe)))

    # uncertainty
    un_exp = xe_exp-precision+1
    un_int = round(xe*10**(-un_exp))

    # nominal value
    no_exp = un_exp
    no_int = round(x*10**(-no_exp))

    # format - nom(unc)exp
    fieldw = x_exp - no_exp
    fmt = '%%.%df' % fieldw
    result1 = (fmt + '(%.0f)e%d') % (no_int*10**(-fieldw), un_int, x_exp)

    # format - nom(unc)
    fieldw = max(0, -no_exp)
    fmt = '%%.%df' % fieldw
    result2 = (fmt + '(%.0f)') % (no_int*10**no_exp, un_int*10**max(0, un_exp))

    # return shortest representation
    if len(result2) <= len(result1):
        return result2
    else:
        return result1
