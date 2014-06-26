from numpy import *
from matplotlib import pyplot as plt

import inc.constants as C
import inc.signal

from inc.tools import *
from inc.inertia import *

import json

# Calculation section
workdir = "data/Inertia"
filename = "{}/TimeTest.json".format(workdir)

with open(filename, 'r') as fp:
	Data = json.load(fp)

R  = array(Data['positions'])
Mt = Data['test mass']
p0 = Data['initial parameters']

It = Mt * R**2

for s in Data['series']:
	I = GetISeries(workdir, s, Mt + C.Mp, Mt, R, p0, It)

plt.show()
