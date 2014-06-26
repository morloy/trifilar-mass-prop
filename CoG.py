from numpy import *
from matplotlib import pyplot as plt

import inc.constants as C
import inc.share as S
from inc.tools import *
from inc.cog import *

import json

filename = "data/CoG/3Mass.json"

with open(filename, 'r') as fp:
	Data = json.load(fp)

R = array(Data['positions'])
Mu = Data['unit mass']
Mt = Data['test mass']

name     = Data['data']['name']
free_arm = Data['data']['free arm']
series   = Data['data']['series']

GetCoG2DSeries(name, free_arm, series, Mu, Mt, R)

plt.show()
