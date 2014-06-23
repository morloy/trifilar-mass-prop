from numpy import *
import os
import scipy.constants


import constants as C
from tools import *
import signal
import cog
import json

class Inertia:
	Mp = 0.			# platform mass
	Mu = 0.			# unit mass
	n = 0

	R = []
	Data = []
	Platform = []

	workdir = ""

	def __init__(self, filename):
		self.workdir = os.path.split(filename)[0]

		with open(filename, 'r') as fp:
			self.Data = json.load(fp)

		self.Mp = self.Data['platform mass']
		self.Mu = self.Data['unit mass']
		self.R = self.Data['positions']
		self.n = len(self.Data['positions'])

		s = self.Data['cog']['series']
		G1 = cog.GetCoG(s['y']['unit'], s['y']['platform'], s['y']['free arm'], self.Mu)
		G2 = cog.GetCoG(s['z']['unit'], s['z']['platform'], s['z']['free arm'], self.Mu)

		print cog.GetCoG3D(G1, G2, self.Data['cog']['axes'])

		self.Platform = self.GetInertiaSeries(self.Data['platform series'], self.Mp)

	def GetInertiaTensor(self):
		I = {}

		I['xx'] = self.GetAxisInertia('xx')
		I['yy'] = self.GetAxisInertia('yy')
		I['zz'] = self.GetAxisInertia('zz')

		# Diagonal elements
		It = self.GetAxisInertia('xy')
		I['xy'] = It - (I['xx'] + I['yy']) / 2.

		It = self.GetAxisInertia('xz')
		I['xz'] = It - (I['xx'] + I['zz']) / 2.

		It = self.GetAxisInertia('yz')
		I['yz'] = It - (I['yy'] + I['zz']) / 2.	def GetInertiaSeries(self, name, m):
		LI = []

		for r in self.R:
			filename = "{}_{}".format(name, r)
			T = signal.GetPeriod( os.path.join(self.workdir, filename) )
			LI += [ C.R**2 / ( (2*pi)**2 * C.L) * scipy.constants.g * m * T**2 ]

		return I

	def GetInertiaSeries(self, name, m):
		LI = []

		for r in self.R:
			filename = "{}_{}".format(name, r)
			T = signal.GetPeriod( os.path.join(self.workdir, filename) )
			LI += [ C.R**2 / ( (2*pi)**2 * C.L) * scipy.constants.g * m * T**2 ]

		return array(LI)

	def GetDiffInertia(self, series):
		LI = series - self.Platform

		StatPrint("I", LI)

		return mean(LI)

	def GetAxisInertia(self, axis):
		print "Axis {}:".format(axis)
		Iup = self.GetInertiaSeries(axis, self.Mu + self.Mp)

		Ip = self.GetDiffInertia(Iup)
		return Ip
