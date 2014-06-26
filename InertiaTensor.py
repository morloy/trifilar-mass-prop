from numpy import *
from matplotlib import pyplot as plt

import inc.constants as C
import inc.share as S
import inc.signal

from inc.tools import *
from inc.inertia import *
from inc.cog import *
from pprint import pprint

import json


workdir = "data/InertiaTensor"
filename = "{}/FFU.json".format(workdir)

with open(filename, 'r') as fp:
	Data = json.load(fp)

Mp = Data['platform mass']
Mu = Data['unit mass']
Mt = Data['test mass']
R  = array(Data['positions'])
p0 = Data['initial parameters']

X = linspace(R[0],R[-1], 20)
gt = lambda R: Mt * R / C.R
It = lambda R: Mt * R**2

axes    = Data['cog']['axes']
CoGData = Data['cog']['data']

CoG3D = GetCoG3DSeries(axes, CoGData, Mu, Mt, R)
CoG3D = mean(CoG3D, axis=0)

ToI   = GetInertiaTensorSeries(workdir, Mu, Mp, Mt, R, p0, CoG3D)

# Final plotting section
#plt.show()
