from numpy import *
import os, sys, json

import inc.constants as C
from inc.tools import *
from inc.cog import *

from matplotlib import pyplot as plt

def Plot(g, gp, name):
	#plt.plot(R, g, 'x', label=name,)
	plt.plot(R, g-gt, label="{}-gt".format(name))

S.Plot['GetG'] = Plot


filename = "data/CoG/SingleScale.json"
with open(filename, 'r') as fp:
	Data = json.load(fp)

Mt = Data['test mass']
R  = array( Data['positions'] )
gt = Mt * R / C.R

for D in Data['series']:
	data = D['data']

	GetG(data, gt * 1000)

#plt.plot(R,gt,label=r"$g_{theo}$")

plt.title("Single scale calibration")
plt.xlabel("r [m]")
plt.ylabel(r"$\Delta g$ [g]")
plt.legend(loc="best")
plt.savefig("out.pdf")
plt.show()
