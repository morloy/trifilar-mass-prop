from tools import *

def GetCoG(unit, platform, free_arm, m):
	g = array(unit) - array(platform)

	for i in xrange(2):
		StatPrint("g[{}]".format(i), g[i])
	
	g = mean(g, axis=1)


	if free_arm == 1:
		G = [ 0., g[0], g[1] ]
	elif free_arm == 2:
		G = [ g[0], 0., g[1] ]
	elif free_arm == 3:
		G = [ g[0], g[1], 0. ]
	else:
		print "Unsupported free arm!"

	return (G[0]*C.Sv[0] + G[1]*C.Sv[1] + G[2]*C.Sv[2]) / m
	
def GetCoG3D(G1, G2, axes):
	if axes == "xy":
		G = [ G2[0], G1[1], (G1[0] + G2[1]) / 2. ]
	elif axes == "xz":
		G = [ G2[0], (G1[1] + G2[1]) / 2., G1[0] ]
	elif axes == "yz":
		G = [ (G1[0] + G2[0]) / 2., G2[1], G1[1] ]
	else:
		print "Unsupported CoG orientation!"
		G = False
	
	return G

