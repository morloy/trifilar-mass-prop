import constants as C

from numpy import *
from numpy.linalg import *
import scipy.constants

import sys
from os.path import basename, isdir, splitext
from os import listdir




def angle(a, b):
    return arccos( dot(a,b) / ( norm(a) * norm(b) ) )

def pol2xy(r,theta):
    return array([ r*cos(theta), r*sin(theta) ])

def CoG(G, m):
    # Apply calibration
    for i in xrange(len(G)):
        if G[i]:
            G[i] += C.CorrG[i][0]*G[i] + C.CorrG[i][1]

    # Calculate CoG
    cog = (G[0]*C.Sv[0] + G[1]*C.Sv[1] + G[2]*C.Sv[2]) / m

    # Calculate errorfrom
    err_g = ( bool(G[0] > 0)*absolute( C.Sv[0] )   \
              + bool(G[1] > 0)*absolute( C.Sv[1] ) \
              + bool(G[2] > 0)*absolute( C.Sv[2] )
            ) * C.Dg / m
    err_R = absolute(cog*C.DR/C.R)
    err_m = absolute(cog*C.DM/m)
    err = err_g + err_R + err_m
    #print "CoG errors:", err_g, err_R, err_m, err
    #print "CoG error:", err/absolute(cog)*100.

    return cog

def k(CoGv):
    Rv = [
            C.Sv[0] - CoGv,
            C.Sv[1] - CoGv,
            C.Sv[2] - CoGv,
    ]

    a1 = angle(Rv[1], Rv[2])
    a2 = angle(Rv[0], Rv[2])
    a3 = angle(Rv[0], Rv[1])
    
    R1 = norm(Rv[0])
    R2 = norm(Rv[1])
    R3 = norm(Rv[2])

    f = R1*R2*R3 * ( R1*sin(a1) + R2*sin(a2) + R3*sin(a3) ) / ( R2*R3*sin(a1) + R1*R3*sin(a2) + R1*R2*sin(a3) )

    #return f / ( (2*pi)**2 * C.L)
    return C.R**2 / ( (2*pi)**2 * C.L)

def I(CoG, M, T):
    return k(CoG) * scipy.constants.g * M * T**2 - M * norm(CoG)**2

# build file list from arguments
# directories will be scanned for files with given extension
def get_file_list(paths, ext):
    files = []
    for arg in paths:
        if isdir(arg):
            # scan for files
            for f in listdir(arg):
                if splitext(f)[1].lower() == ext:
                    files += [ arg+f ]
        else:
            files += [ arg ]

    return files

# Returns Theta coordinate of arm 1-3
def Arm_T(arm):
    Arm_T = array([ 1, 2, 0 ]) * 2.*pi/3

    return Arm_T[arm-1]

# Returns vectors p and r for a line defined by
# l(t) = p + t*r
def Line(CoG, axis='zz'):
    if axis == 'xx':
        p = array([ 0., CoG[1], CoG[0] ])
        r = array([ 1., 0., 0. ])
    elif axis == 'yy':
        p = array([ CoG[0], 0., CoG[1] ])
        r = array([ 0., 1., 0. ])
    # zz axis
    else:
        p = array([ CoG[0], CoG[1], 0. ])
        r = array([ 0., 0., 1. ])

    return array([ p, r ])


def ClosestPoint(L1, L2):
    # Adapted from
    # http://geomalgorithms.com/a07-_distance.html

    a = dot(L1[1], L1[1])
    b = dot(L1[1], L2[1])
    c = dot(L2[1], L2[1])

    w0 = L2[0] - L1[0]
    d = dot(L1[1], w0)
    e = dot(L2[1], w0)

    s = (b*e - c*d) / (a*c - b**2)
    t = (a*e - b*d) / (a*c - b**2)
    print a,b,c,d,e,s,t,w0

    Ps = L1[0] - s*L1[1]
    Qt = L2[0] - t*L2[1]
    print Ps, Qt

    wc = Ps - Qt
    print wc
    print dot(L1[1], wc)
    print dot(L2[1], wc)

    return (Ps + Qt) / 2

def StatPrint(name, D):
		print "{}: {} +/- {}".format(name, mean(D), std(D))


def StatPrint(name, D):
		print "{}: {} +/- {}".format(name, mean(D), std(D))
