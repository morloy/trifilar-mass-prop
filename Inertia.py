from numpy import *
from matplotlib import pyplot as plt

import inc.constants as C
import inc.signal

from inc.tools import *
from inc.inertia import *

import json

def Plot(workdir, name, m, R, p0, Ip, Iup, Iu):
	global It

	plt.plot(R, Iup - mean(Iu),'x', label="I-Ip")
	plt.plot(R, It, label="It")

S.Plot['GetI'] = Plot


workdir = "data/Inertia"
filename = "{}/TimeTest.json".format(workdir)

with open(filename, 'r') as fp:
	Data = json.load(fp)

R  = array(Data['positions'])
Mt = Data['test mass']
p0 = Data['initial parameters']

It = Mt * R**2

for s in Data['series']:
	I = GetI(workdir, s, Mt + C.Mp, R, p0, It)

	plt.title("Inertia Test {}".format(s))

	#plt.rc('text', usetex=True)
	plt.xlabel(r'$r~[cm]$')
	plt.ylabel(r'$I~[kg~m^2]$')
	plt.margins(.05)
	plt.legend(loc="best")

plt.savefig("out/out.pdf")
plt.show()
