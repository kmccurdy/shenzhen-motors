# class to simulate XLoBorg sensor readouts

import math
import random
import time


# classes for simulation

class SimXLo:
	def __init__(self):
		self.targetAngle = 0
		self.targetCoords = (0, 0, 1)
		self.currentCoords = (0, 0, 0) 
		self.defaultSteps = 6
		self.defaultTimeStep = .5 # default time step between steps in seconds

	# sets target angle from input in degrees (0-360)
	def set_target(self, targetAng):
		self.targetAngle = targetAng
		self.targetCoords = angle_to_cartesian(targetAng)

	# interpolates and updates values from one angle to another
	def sim_rotate(self, steps=None, timeStep=None):
		if not steps:
			steps = self.defaultSteps
		if not timeStep:
			timeStep = self.defaultTimeStep
		start = self.currentCoords
		end = self.targetCoords
		distance = [float(e - s) for s, e in zip(start, end)]
		print 'Current:', start, 'Target:', end
		for i in range(steps + 1):
			currentDist = [d * i/steps for d in distance]
			newCoords = tuple([d + st for d, st in zip(currentDist, start)])
			self.currentCoords = newCoords
			print 'Current:', self.currentCoords
			time.sleep(timeStep)

	def ReadAccelerometer(self):
		return jit(self.currentCoords)

# helpers

# add jitter to a set of coordinates
def jit(coords):
	coords = tuple([point + random.uniform(-.1, .1) for point in coords])
	return coords

# input angle to cartesian coordinates
def angle_to_cartesian(target):
	# convert target angle to radians
	targetRad = float(target)/360 * 2 * math.pi
	# convert target angle to cartesian coordinates
	# using a constant distance R of 1. TODO: check that this is okay
	Ccoords = cartesian(R=1, F=targetRad)
	return Ccoords;

# cylindrical polar coordinates to cartesian
# http://electron9.phys.utk.edu/vectors/3dcoordinates.htm
def cartesian(R, F, Z=0):
    x = R * math.cos(F)
    y = R * math.sin(F)
    z = Z # don't bother - isn't used
    return (x, y, z)

"""
test commands:
import SimXLo as sim
x = sim.SimXLo()
x.set_target(10)
x.sim_rotate()

"""

