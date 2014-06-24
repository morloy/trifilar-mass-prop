from numpy import *
import os
import scipy.constants


import constants as C
import share as S
from tools import *
import signal
import cog
import json

from pprint import pprint

def GetInertiaSeries(workdir, name, m, R, p0):
	I = []

	for r in R:
		filename = "{0}/{1}/{2:.2f}".format(workdir, name, r)
		T = signal.GetPeriod(filename, p0)
		I += [ C.R**2 / ( (2*pi)**2 * C.L) * scipy.constants.g * m * T**2 ]

	return array(I)

def GetI(workdir, name, m, R, p0, Ip):
	Iup = GetInertiaSeries(workdir, name, m, R, p0)
	Iu = Iup - Ip

	StatPrint("I_{}".format(name), Iu * 1000)
	S.Plot['GetI'](workdir, name, m, R, p0, Ip, Iup, Iu)

	return mean(Iu) * 1000

def GetInertiaTensor(workdir, Mu, Mp, R, p0):
	Ip = GetInertiaSeries(workdir, "platform", Mp, R, p0)
	print Ip

	I = {}
	for axis in ["xx", "yy", "zz", "xy", "xz", "yz"]:
		I[axis] = GetI(workdir, axis, Mu + Mp, R, p0, Ip)
	
	I['xy'] -= (I['xx'] + I['yy']) / 2.
	I['xz'] -= (I['xx'] + I['zz']) / 2.
	I['yz'] -= (I['yy'] + I['zz']) / 2.

	pprint(I)

	return I
	def GetAxisInertia(axis, Mup, R, platform, workdir):
		print "Axis {}:".format(axis)
		Iup = GetInertiaSeries(axis, Mup, R, workdir)
		Ip = GetDiffInertia(Iup, platform)

		return Ip
