from Tools import *

# Constants

# Distances [m]
R = 1.     # support points to geometric center
L = .995    # Length of the cables
Rg = .995   # g measure points to geometric center

# Weights   [kg]
Mp = 0.848             # platform bare

# Errors
DR = DL = .5e-3
Dg  = 0.10e-3
DM = 0.005e-3

# Support points
S1v = pol2xy(R, 2.*pi/3)        # arm 1
S2v = pol2xy(R, 4.*pi/3)        # arm 2
S3v = pol2xy(R, 0.)             # arm 3

Sv = array([
    pol2xy(R, 2.*pi/3),
    pol2xy(R, 4.*pi/3),
    pol2xy(R, 0.)
])

# Arm unit vectors
a1 = pol2xy(1., 2.*pi/3)
a2 = pol2xy(1., 4.*pi/3)
a3 = pol2xy(1., 0.)


# Platform calibration

# CoG measures [kg]
#Gp = array([ 0., 1.81, 4.09 ]) * 1e-3
#Gp = array([ 0., 1.68, 4.05 ]) * 1e-3
Gp = array([ 0., 0., 0. ]) * 1e-3
#Gp = array([ 0., 1.97, 4.70 ]) * 1e-3

# CoG Vector
CoGp = CoG(Gp,Mp)
print "Platform CoG:", CoGp

# Periods [s]
Tp = 1.01386594017     # platform

# Inertia
Ip = I(CoGp, Mp, Tp)
Ip = 0.234478887577	# new experimental value

print "Platform Moment:",Ip

# Video FPS
fps = 240

# CoG calibration
CorrG = array([
    #  A           B
    [  0.00026799, -0.00190250 ],   # arm 1
    [  0.00032392, -0.00163896 ],   # arm 2
    [ -0.04125201, -0.00390974 ],   # arm 3
])
CorrG = array([
    #  A           B
    [  0., -0.00190250 ],   # arm 1
    [  0., -0.00163896 ],   # arm 2
    [ -0.04125201, -0.00390974 ],   # arm 3
])
