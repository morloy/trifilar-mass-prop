import constants as C

from numpy import *
from numpy.linalg import *
import scipy.constants

import sys
from os.path import basename, isdir, splitext
from os import listdir

def pol2xy(r,theta):
    return array([ r*cos(theta), r*sin(theta) ])

def StatPrint(name, D):
	print "{}: {} +/- {}".format(name, mean(D), std(D)/sqrt(len(D)) )
