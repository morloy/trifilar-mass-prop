"""Helper function to analyze csv files from videos."""

import constants as C

from numpy import *
from scipy.optimize import curve_fit

from scipy.fftpack import *

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from os.path import isfile
from subprocess import call

i = 0
p0Last = []

def GetPeriod(name, p0 = [100., 1e-1, 1., .1, 10., 1., 1., .1, 100.]):
	"""Returns the period of oscillation from a given filename, corresponding to a csv or movie file.
	If no csv file exist, the tracker program is called to analyze the video.

	Parameters
	----------
	name : str
		Filename WITHOUT extension.
	p0 : array_like
		Initial parameters for the least-square fit given in the order
		A1, tau1, T1, d1, A2, tau2, T2, d2, C 
	
	Returns
	-------
	T : float
		Period of oscillation in seconds.
	TErr : float
		Standard deviation of the period estimate.
	"""
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


	try:
		coeff, var_matrix = curve_fit(func, t, x, p0=p0)
		p0Last += [ coeff ]
	except RuntimeError:
		print "Last successful initial parameters:"
		for p0 in p0Last:
			print "[ {} ]".format(', '.join(map(str,p0)))
		raise

	# select period with biggest amplitude
	w = 2 + 4*argmax( absolute((coeff[0], coeff[4])) )
	T = abs(coeff[w])
	TErr = sqrt(var_matrix[w,w])
	#print "T: {} +/- {}, samples: {}".format(T, sqrt(var_matrix[2,2]), len(x)) 

	if (0):
		i += 1
		if i == 32:
			xt = func(t, *coeff)
			m = mean(x)

			fig = plt.figure(i, figsize=(6, 9))
			plt.rc('font', size=12)
			s = 1e-1

			plt.subplot(3, 1, 1)
			FftRes = abs(rfft(x - m))/sqrt(len(x))
			Hz = linspace(0, C.fps/2., len(x))
			plt.plot(Hz, FftRes*s)
			plt.xlim(0,2)
			plt.xlabel(r'$f\,[\mathrm{Hz}]$')
			plt.ylabel(r'$|\mathcal{F}(f)|$')
			plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))
			plt.title(r'signal spectrum')

			plt.subplot(3, 1, 2)
			plt.plot(t, (x  - m)*s,'.')
			plt.plot(t, (xt - m)*s)
			plt.xlabel(r'$t\,[\mathrm{s}]$')
			plt.ylabel(r'$x$')
			plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))
			plt.title(r'signal with fit')

			plt.subplot(3, 1, 3)
			plt.plot(t, (xt - x)*s)
			plt.xlabel(r'$t\,[\mathrm{s}]$')
			plt.ylabel(r'$x$')
			plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))
			plt.title(r'residual')

			plt.tight_layout()
			plt.show()

	return T, TErr
