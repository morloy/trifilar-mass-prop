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
R  = Data['positions']
p0 = Data['initial parameters']

axes    = Data['cog']['axes']
CoGData = Data['cog']['data']

CoG3D = GetCoG3D(axes, CoGData, Mu)
ToI   = GetInertiaTensor(workdir, Mu, Mp, R, p0)
