from matplotlib import pyplot as plt
from tools import *
import share as S

def GetCoG3D(axes, D, m):

	G = zeros((2,2))
	for i in xrange(2):
		G[i] = GetCoG2D(D[i]['name'], D[i]['free arm'], D[i]['series'], m)

	if axes == "xy":
		G = [ G[1][0], G[0][1], (G[0][0] + G[1][1]) / 2. ]
	elif axes == "xz":
		G = [ G[1][0], (G[0][1] + G[1][1]) / 2., G[0][0] ]
	elif axes == "yz":
		G = [ (G[0][0] + G[1][0]) / 2., G[1][1], G[0][1] ]
	else:
		print "Unsupported CoG orientation!"
		G = False

	
	print "CoG3D: {} [mm]".format(array(G) * 1000)

	return G

def GetG(data, platform, name="g"):
	g = array(data) * 1e-3
	gp = array(platform) * 1e-3

	StatPrint(name, g-gp)
	S.Plot['GetG'](g, gp, name)
	return mean(g-gp)

def GetCoG2D(name, free_arm, S, m):
	print "\n{}:".format(name)

	G = zeros(2)
	for i in xrange(2):
		G[i] = GetG(S[i]['data'], S[i]['platform'], S[i]['name'])

	if free_arm == 1:
		G = [ 0., G[0], G[1] ]
	elif free_arm == 2:
		G = [ G[0], 0., G[1] ]
	elif free_arm == 3:
		G = [ G[0], G[1], 0. ]
	else:
		print "Unsupported free arm!"

	# Calculate Center of Gravity
	G = (G[0]*C.Sv[0] + G[1]*C.Sv[1] + G[2]*C.Sv[2]) / m

	print "CoG2D: {} [mm]\n".format(G * 1000)

	return G
