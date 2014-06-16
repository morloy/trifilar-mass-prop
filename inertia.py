from numpy import *
from scipy import *
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.constants import *
from numpy.linalg import *

import os.path

# local files
from Constants import *
from Tools import *
from Signal import *


csv = sys.argv[1]

workdir = os.path.split(csv)[0]

data = genfromtxt(csv, skip_header=1, dtype="S20,f,f,f,f,f")

# Manually create array, if only one entry in csv
if len(data.shape) == 0:
    data = array([ data])

R = []
T = []
LI = []
LIt = []
for D in data:
    name = D[0]
    Mu = D[1] + Constants.Mp
    Gu = array([ D[2], D[3], D[4] ]) 
    Itu = D[5]


    R += [ int(name) ]

    # Unit CoG
    CoGu = CoG(Gu, Mu)

    Tu = get_period( os.path.join(workdir,name) )
    T += [ Tu ]

    # Unit inertia
    Iu = I(CoGu, Mu, Tu)
    LI += [ Iu ]
    LIt += [ Itu ]

    if (0):
        print "Name: {}".format(name)
        print "Unit CoG:", CoGu
        print "Iu:", Iu
        print "It:", Itu
        print

T = array( T )
LI = array( LI )
LIt = array( LIt )

Ip = mean(LI-LIt)
#Ip = 0.234519658105
0.234478887577

err = absolute(LI-Ip-LIt)

print "Ip: {} +/- {}".format(Ip, std(LI-LIt))
print "I:", LI-Ip
print "err:", err
print "err (mean): {} +/- {}".format(mean(err), std(err))
#print "rel err:", absolute(LI-Ip-LIt) / LIt * 100
plt.figure(1)
plt.title("calibration 20s")
plt.plot(R, LI-Ip,'x', label="LI-Ip")
plt.plot(R, LIt, label="LIt")
plt.plot(R, absolute(LI-Ip-LIt), label="error" )

plt.rc('text', usetex=True)
plt.xlabel(r"$r~[cm]$")
plt.ylabel(r"$I~[kg~m^2]$")
plt.margins(.05)
plt.legend(loc="best")
plt.show()

"""
# cylinder
    Mub = 2.385  # unit bare
    Rdisk = 0.138
    Tu = 0.548327277151
    It = .5 * Mub * Rdisk**2
"""
