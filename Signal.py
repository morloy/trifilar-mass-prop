import Constants

from numpy import *
from scipy.optimize import curve_fit

from matplotlib import pyplot as plt

from os.path import isfile
from subprocess import call


i=2

def get_period(name):
    global i
    csv = "{}.csv".format(name)

    # Analyze video, if .csv not already present
    if not isfile(csv):
        mp4 = "{}.MP4".format(name)
        print "Analyzing video file:"

        call(["./track", mp4])

    data = genfromtxt(csv, names=True)

    x = data['x']
    t = arange(0., len(x)) / Constants.fps


    # fit wave function
    def func(t, *p):
        A1, tau1, T1, d1, A2, tau2, T2, d2, C = p
        return A1 * exp(-tau1*t) * sin(2*pi/T1*t+d1) + A2 * exp(-tau2*t) * sin(2*pi/T2*t+d2) + C

    p0 = [100., 1e-1, 1., .1, 10., 1., 1., .1, 100.]
    p0 = [  1.07272135e+02,   1.13750393e-02,   1.05117156e+00,   2.98843257e+00,  1.20129085e+01,   7.91008021e-03,  -2.00064377e+00,   1.32985413e+01, 5.28854196e+02]

    coeff, var_matrix = curve_fit(func, t, x, p0=p0)
    #print coeff
    T = min( absolute((coeff[2], coeff[6])) )
    print "T: {} +/- {}, samples: {}".format(T, sqrt(var_matrix[2,2]), len(x)) 

    xt = func(t, *coeff)
    err = xt - x
    if (1):
	    plt.figure(i)
	    i += 1
	    #plt.title(name)
	    plt.plot(t,x,'.', label='data')
	    plt.plot(t,xt, label='fit')
	    plt.plot(t,err, label='error')
	    plt.legend(loc='best')
	    #plt.show()

    return T
