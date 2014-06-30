"""All functions related to the center of gravity."""

from matplotlib import pyplot as plt

from constants import *
from tools import *


def GetCoG3D(axes, G):
	"""Returns the 3D CoG for 2 different 2D CoG measurements in the given 
	axis configuration.

	Parameters
	----------
	axes : str
		String describing the two axes, in which the measurements were taken.
		Can be one of 'xy', 'xz' and 'yz'.
	G : ndarray
		A 2x2 array giving two 2D CoG coordinates. G[0] is the first CoG, G[1] the second.
	
	Returns
	-------
	R : ndarray
		The 3D center of gravity
	"""

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
	"""Return the full 3D CoG series for a given measurements series.

	Parameters
	----------
	axes : str
		String describing the two axes, in which the measurements were taken.
		Can be one of 'xy', 'xz' and 'yz'.
	D : array_like
		A 3D CoG measurement series as read from the JSON file, see examples.
	
	Returns
	-------
	R : ndarray
		Array containing x, y and z coordinate of the 3D CoG.
		Each entry contains n values for the complete series.

	Examples
	--------

	>>> import json
	>>> D = json.loads('''
	{
		"cog": {
			"axes": "xz",
			"data": [
				{
					"name": "R_x",
					"free arm": 2,
					"series": [
						{
							"name": "g_{x,1}",
							"data": [ 4.95, 6.03, 7.08, 8.14, 9.26 ],
							"platform": [ 2.11, 3.09, 4.13, 5.20, 6.27 ]
						},
						{
							"name": "g_{x,3}",
							"data": [ 7.35, 8.46, 9.48, 10.54, 11.60 ],
							"platform": [ 6.49, 7.54, 8.61, 9.67, 10.70 ]
						}
					]
				},
				{
					"name": "R_z",
					"free arm": 1,
					"series": [
						{
							"name": "g_{z,2}",
							"data": [ 2.92, 3.99, 5.05, 6.14, 7.18 ],							
							"platform": [ 2.19, 3.25, 4.29, 5.38, 6.52 ]						
						},
						{
							"name": "g_{z,3}",
							"data": [ 5.50, 6.61, 7.74, 8.84, 10.07 ],
							"platform": [ 6.45, 7.53, 8.59, 9.67, 10.72 ]
						}
					]
				}
			]
		}
	}
	''')
	>>> pprint(D)
	[{u'free arm': 2,
	  u'name': u'R_x',
	  u'series': [{u'data': [4.95, 6.03, 7.08, 8.14, 9.26],
				   u'name': u'g_{x,1}',
				   u'platform': [2.11, 3.09, 4.13, 5.2, 6.27]},
				  {u'data': [7.35, 8.46, 9.48, 10.54, 11.6],
				   u'name': u'g_{x,3}',
				   u'platform': [6.49, 7.54, 8.61, 9.67, 10.7]}]},
	 {u'free arm': 1,
	  u'name': u'R_z',
	  u'series': [{u'data': [2.92, 3.99, 5.05, 6.14, 7.18],
				   u'name': u'g_{z,2}',
				   u'platform': [2.19, 3.25, 4.29, 5.38, 6.52]},
				  {u'data': [5.5, 6.61, 7.74, 8.84, 10.07],
				   u'name': u'g_{z,3}',
				   u'platform': [6.45, 7.53, 8.59, 9.67, 10.72]}]}]
	'''
	"""
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
	"""Return the g value of a measurements.

	Parameters
	----------
	data : array_like
		The measured g values in gram.
	platform : array_like
		The measured bare platform g values in gram.
	Mt : float
		Test mass
	R : ndarray
		The measurements positions in m.
	name : str
		Name for the measurement, may contain LaTeX.
	
	Returns
	-------
	g : ndarray
		The bare unit g values.
	"""
	gup = array(data) * 1e-3
	gp = array(platform) * 1e-3

	PlotGTest(gup, Mt, R, name)
	PlotGTest(gp, Mt, R, name+"'")

	g = gup - gp

	StatPrint(name, g * 1000, "g")

	return g

# Plotting section
def PlotGTest(g, Mt, R, name):
	"""Creates a plot for a g value measurements series in the 'out' folder.

	Parameters
	----------
	g : array_like
		The measured g values in gram.
	Mt : float
		Test mass
	R : ndarray
		The measurements positions in m.
	name : str
		Name for the measurement, may contain LaTeX.
	"""
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
	"""Calculate 2D center of gravity from a single measurement on two arms.

	Parameters
	----------
	G : ndarray
		The 2 g values for the measured arms.
	free_arm : int
		Number indicating the free arm, may be one of 1, 2 and 3.
	m : float
		The mass of the system.
	
	Returns
	-------
	ndarray
		The 2D CoG of the system.
	"""
	if free_arm == 1:
		return (G[0]*C.Sv[1] + G[1]*C.Sv[2]) / m
	elif free_arm == 2:
		return (G[0]*C.Sv[0] + G[1]*C.Sv[2]) / m
	elif free_arm == 3:
		return (G[0]*C.Sv[0] + G[1]*C.Sv[1]) / m
	else:
		print "Unsupported free arm!"


def GetCoG2DSeries(name, free_arm, S, M, Mt, R):
	"""Returns the series of 2D CoGs for a given measurement series.

	Parameters
	----------
	name : str
		Name for the measurement, may contain LaTeX.
	free_arm : int
		Number indicating the free arm, may be one of 1, 2 and 3.
	M : float
		System mass
	Mt : float
		Test mass
	D : array_like
		A 3D CoG measurement series as read from the JSON file, see examples.
	R : ndarray
		The measurements positions in m.

	Returns
	-------
	R : ndarray
		Array containing x, y coordinates of the 2D CoG.
		Each entry contains n values for the complete series.

	Examples
	--------

	>>> import json
	>>> S = json.loads('''
	{
		"name": "R_x",
		"free arm": 2,
		"series": [
			{
				"name": "g_{x,1}",
				"data": [ 4.95, 6.03, 7.08, 8.14, 9.26 ],
				"platform": [ 2.11, 3.09, 4.13, 5.20, 6.27 ]
			},
			{
				"name": "g_{x,3}",
				"data": [ 7.35, 8.46, 9.48, 10.54, 11.60 ],
				"platform": [ 6.49, 7.54, 8.61, 9.67, 10.70 ]
			}
		]
	}
	''')
	>>> pprint(S)
	[{u'data': [4.95, 6.03, 7.08, 8.14, 9.26],
	  u'name': u'g_{x,1}',
	  u'platform': [2.11, 3.09, 4.13, 5.2, 6.27]},
	 {u'data': [7.35, 8.46, 9.48, 10.54, 11.6],
	  u'name': u'g_{x,3}',
	  u'platform': [6.49, 7.54, 8.61, 9.67, 10.7]}]

	"""
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
