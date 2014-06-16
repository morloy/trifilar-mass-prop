from numpy import *
from numpy.linalg import *
from matplotlib import pyplot as plt

from scipy.optimize import curve_fit

from Constants import *
from Tools import *


for csv in sys.argv[1:]:
    print "\n{}:".format(csv)

    data = genfromtxt(csv, comments='#')

    X = []
    Y = []
    Err = []
    #print "CoGt\t\tCoGb\t\terr\t\tgt\t\tg\t\terr"
    for m, r, g in data:
        g *= 1e-3
        #g += -0.88468911*g -0.00047023
        m *= 1e-3

        # Theoretical CoG
        CoGt = m*r / (Mp + m)
        gt = m * r / R

        # Measured CoG
        CoGb = g*R / (Mp + m)
        
        err_cog = abs(CoGb - CoGt)
        err_g = gt - g
        #print "{:.6f}\t{:.6f}\t{:.2e}\t{:.6f}\t{:.6f}\t{:+.2e}".format(CoGt, CoGb, err_cog, gt, g, err_g )

        X   += [ g ]
        Y   += [ gt ]
        Err += [ err_g ]

    X = array(X)
    Y = array(Y)
    Err = array(Err)

    def func(t, *p):
        A, B = p
        return A*t + B
    p0 = [ 0.1, 1.]

    coeff, var_matrix = curve_fit(func, X, Err, p0=p0)

    print "A = {:.8f} +/- {:.2e}, B = {:.8f} +/- {:.2e}".format(coeff[0], sqrt(var_matrix[0,0]), coeff[1], sqrt(var_matrix[1,1]))

    plt.plot(X,func(X,*coeff))
    #plt.plot(X,Y,'.')
    plt.plot(X,Err,'.')

plt.show()
