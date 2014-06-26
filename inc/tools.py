import constants as C
import share as S

from numpy import *
from numpy.linalg import *
import scipy.constants

import os, sys, re
from os.path import splitext

from matplotlib import pyplot as plt

def pol2xy(r,theta):
    return array([ r*cos(theta), r*sin(theta) ])

def StatPrint(name, D, unit='', plot=False, rel=True):
	global fig1, ax1, count, labels
	m = mean(D)
	s = std(D)
	perc = "({:.2f} %)".format(abs(s/m*100))
	if unit <> '':
		unit = '[{}]'.format(unit)
	print "{:<8} {:>17} +/- {:<17} {:>10} {:<10} {:<30}".format(name+':', m, s, perc, unit, D)

def Savefig(fig, name):
	out = "out"
	name_filtered = re.sub(r"[^A-Za-z0-9-]+", '', name.replace("'", "p"))
	script = splitext(sys.argv[0])[0]

	directory = "{}/{}".format(out, script)
	if not os.path.exists(directory):
		os.mkdir(directory)

	fig.savefig("{}/{}/{}.pdf".format(out, script, name_filtered))
