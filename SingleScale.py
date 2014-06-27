from numpy import *
import os, sys, json

import inc.constants as C
from inc.tools import *
from inc.cog import *

from matplotlib import pyplot as plt

# Calculation section
filename = "data/CoG/SingleScale.json"
with open(filename, 'r') as fp:
	Data = json.load(fp)

Mt = Data['test mass']
R  = array( Data['positions'] )

for D in Data['series']:
	g = array(D['data']) * 1e-3
	PlotGTest(g, Mt, R, D['name'])
	StatPrint(D['name'], (g - Mt*R/C.R)*1000, "g")

# Final plotting section
#plt.show()
