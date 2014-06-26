import constants as C

from numpy import *
from scipy.optimize import curve_fit

from matplotlib import pyplot as plt

from os.path import isfile
from subprocess import call

i = 0
p0Last = []

def GetPeriod(name, p0 = [100., 1e-1, 1., .1, 10., 1., 1., .1, 100.]):
	global i, p0Last
	csv = "{}.csv".format(name)

	# Analyze video, if .csv not already present
	if not isfile(csv):
		mp4 = "{}.MP4".format(name)
		print "Analyzing video file:"

		call(["./track", mp4])

	data = genfromtxt(csv, names=True)

	x = data['x']
	t = arange(0., len(x)) / C.fps


	# fit wave function
	def func(t, *p):
		A1, tau1, T1, d1, A2, tau2, T2, d2, C = p
		return A1 * exp(-tau1*t) * sin(2*pi/T1*t+d1) + A2 * exp(-tau2*t) * sin(2*pi/T2*t+d2) + C


	#plt.plot(t,x)
	#plt.show()

	try:
		coeff, var_matrix = curve_fit(func, t, x, p0=p0)
		p0Last += [ coeff ]
	except RuntimeError:
		for p0 in p0Last:
			print "[ {} ]".format(', '.join(map(str,p0)))
		raise

	# select period with biggest amplitude
	T = abs(coeff[2 + 4*argmax( absolute((coeff[0], coeff[4])) ) ])
	#print "T: {} +/- {}, samples: {}".format(T, sqrt(var_matrix[2,2]), len(x)) 

	xt = func(t, *coeff)
	err = xt - x
	if (0):
		plt.figure(i)
		i += 1
		#plt.title(name)
		plt.plot(t,x,'.', label='data')
		plt.plot(t,xt, label='fit')
		plt.plot(t,err, label='error')
		plt.legend(loc='best')
		plt.show()

	return T
