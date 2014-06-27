from matplotlib import pyplot as plt
from tools import *
import share as S

def GetCoG3D(axes, G):
	if axes == "xy":
		R = [ G[1][0], G[0][1], (G[0][0] + G[1][1]) / 2. ]
	elif axes == "xz":
		R = [ G[1][0], (G[0][1] + G[1][1]) / 2., G[0][0] ]
	elif axes == "yz":
		R = [ (G[0][0] + G[1][0]) / 2., G[1][1], G[0][1] ]
	else:
		print "Unsupported CoG orientation!"
	
	return array(R)


def GetCoG3DSeries(axes, D, M, Mt, R):
	G = []
	for i in xrange(2):
		G += [ GetCoG2DSeries(D[i]['name'], D[i]['free arm'], D[i]['series'], M, Mt, R) ]
	G = swapaxes(G,0,1)

	R = []
	D = []
	for g in G:
		r = GetCoG3D(axes, g)
		R += [ r ]
		D += [ sqrt(r[0]**2 + r[1]**2 + r[2]**3) ]
	R = array(R)
	D = array(D)

	print "CoG3D:"
	axes = [ 'x', 'y', 'z']
	for i in xrange(3):
		StatPrint("R_{{{}}}".format(axes[i]), R[:,i] * 1000, "mm")
	StatPrint("D", D*1000, "mm")
	print

	return R

def GetG(data, platform, Mt, R, name="g"):
	gup = array(data) * 1e-3
	gp = array(platform) * 1e-3

	PlotGTest(gup, Mt, R, name)
	PlotGTest(gp, Mt, R, name+"'")

	g = gup - gp

	StatPrint(name, g * 1000, "g")

	return g

# Plotting section
def PlotGTest(g, Mt, R, name):
	X = linspace(R[0],R[-1], 20)
	gt = lambda R: Mt * R / C.R

	fig = plt.figure()
	ax = fig.add_subplot(111)
	fig.tight_layout(pad=1.4)
	ax.plot(R, (g)*1000, 'x', label=r"${0}$".format(name),)
	ax.plot(X, (gt(X)+mean(g-gt(R)))*1000,label=r"$g_t + \Delta g$")
	ax.set_xlabel(r"$r\,[m]$")
	ax.set_ylabel(r"$[g]$")
	#ax.set_title("${}$".format(name))
	ax.margins(.05)
	ax.legend(loc="best")
	Savefig(fig, name)

def GetCoG2D(G, free_arm, m):
	if free_arm == 1:
		return (G[0]*C.Sv[1] + G[1]*C.Sv[2]) / m
	elif free_arm == 2:
		return (G[0]*C.Sv[0] + G[1]*C.Sv[2]) / m
	elif free_arm == 3:
		return (G[0]*C.Sv[0] + G[1]*C.Sv[1]) / m
	else:
		print "Unsupported free arm!"


def GetCoG2DSeries(name, free_arm, S, M, Mt, R):
	print "Series '{}':".format(name)
	n = len(S[0]['data'])

	G = zeros((2,n))
	for i in xrange(2):
		G[i] = GetG(S[i]['data'], S[i]['platform'], Mt, R, S[i]['name'])
	
	G = G.T
	R = zeros((n,2))
	for i in xrange(n):
		R[i] = GetCoG2D(G[i], free_arm, M)

	print "CoG2D:"
	axes = ['x', 'y']
	for i in xrange(2):
		StatPrint("R_{{{}}}".format(axes[i]), R[:,i] * 1000, "mm")
	print

	return R
