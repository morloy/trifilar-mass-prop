import Constants as C

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

    # Calculate error
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

