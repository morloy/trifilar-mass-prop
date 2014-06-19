from numpy import *
from scipy import *
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.constants import *
from numpy.linalg import *

import os.path
import json

# local files
from Constants import *
from Tools import *
from Signal import *


infile = sys.argv[1]

workdir = os.path.split(infile)[0]

with open(infile, 'r') as fp:
	D = json.load(fp)

mp = 1.007				# platform + mounting
m = D['unit mass']
mt = D['test mass']
n = len(D['positions'])

for axis in D['series']:
	LIu = zeros(n)
	LIt = zeros(n)
	print "Axis '{}':".format(axis)

	i = 0
	for rt in D['positions']:
		name = "{}_{}".format(axis, rt)
		T = get_period( os.path.join(workdir,name) )
		Iu = I([0., 0.], m + mp + mt, T)
		
		It = mt * rt**2

		LIu[i] = Iu
		LIt[i] = It
		i += 1

	print LIu
	LI = LIu - LIt
	if (1):
		"""
		plt.plot(LIt)
		plt.plot(LIu - mean(LI), 'x')
		"""
		plt.plot(LI)

	print "I: {} +/- {}".format(mean(LI), std(LI))
	print
plt.show()
