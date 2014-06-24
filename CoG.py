from numpy import *
from matplotlib import pyplot as plt

import inc.constants as C
import inc.share as S
from inc.tools import *
from inc.cog import *

import json

def Plot(g, gp, name):
	global R
	print R, g, gp
	plt.plot(R, g, label="{}".format(name))
	plt.plot(R, gp, label="{}p".format(name))
	#plt.plot(R, g-gp, label="{0}-{0}p".format(name))

S.Plot['GetG'] = Plot


filename = "data/CoG/3Mass.json"

with open(filename, 'r') as fp:
	Data = json.load(fp)

R = Data['positions']
Mu = Data['unit mass']

name     = Data['data']['name']
free_arm = Data['data']['free arm']
series   = Data['data']['series']

GetCoG2D(name, free_arm, series, Mu)

plt.title("CoG Test")
plt.legend(loc="best")
plt.savefig("out/out.pdf")
plt.show()
