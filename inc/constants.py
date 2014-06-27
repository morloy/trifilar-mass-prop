from tools import *
import matplotlib

# Constants

# Distances [m]
R = 1.		# support points to geometric center
L = .995    # Length of the cables
Rg = .995   # g measure points to geometric center

# Weights   [kg]
Mp = 0.848			# platform bare
Mpm = 1.003			# platform + mount

# Errors
DR = DL = .5e-3
Dg  = 0.10e-3
DM = 0.005e-3

# Support points
Sv = array([
    pol2xy(R, 2.*pi/3),		# arm 1
    pol2xy(R, 4.*pi/3),		# arm 2
    pol2xy(R, 0.)			# arm 3
])

# Video FPS
fps = 240

font = {'family' : 'serif',
        'size'   : 18}
matplotlib.rc('font', **font)
