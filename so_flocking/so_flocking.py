from pymel.core.datatypes import Vector
import pymel.core.effects as effects

import math
import itertools

PIBY2 = math.pi / 2

def unflattenFloat3Array(arr):
	"""Unflatten a float3 array representing vectors to a list
	of PyMEL vectors."""

	x, y, z = itertools.islice(arr, 0, None, 3), itertools.islice(arr, 1, None, 3), itertools.islice(arr, 2, None, 3)
	vzip = itertools.izip(x, y, z)

	return [Vector(*x) for x in vzip]

def getParticleIds(shapeName):
	"""Get a list of all the particle ids in a shape.

	Only the active particles are returned, dead particles are
	not in the result set.

	shapeName is either the name of the shape, or its tranform."""

	return effects.getParticleAttr(shapeName, at="particleId", array=True)

def getParticlePositions(shapeName):
	positions = effects.getParticleAttr(shapeName, at="position", array=True)

	return unflattenFloat3Array(positions)

def vectorAverage(vectors):	
	"""Get the average vector for a list of vectors."""

	# Todo type checking? Perhaps. Or just catch and whine on TypeError.

	return reduce(lambda x, y: x + y, vectors) / len(vectors)

def inFov(pos, viewDir, pos2, fov=math.pi):
	line = pos2 - pos

	d = line.dot(viewDir)
	# Quickly eliminate perpendiculars and orthogonals:
	if d == 1:
		return True
	if fov >= PIBY2 and d == 0:
		return True
	if fov >= math.pi and d == -1:
		return True

	# We should think about floating point calculations here.

	ang = math.acos(d)
	return ang <= fov

def inRadius(pos, pos2, radius):
	line = pos - pos2

	return line.length() <= radius

class ParticlesFrameData(object):

	def __init__(self, shapeName):
		super(ParticlesFrameData, self).__init__()
		self.__shapeName = shapeName
		self.__data = dict()
		self.__ids = getParticleIds(self.__shapeName)
	
	def loadAttribute(self, attributeName, float3Array=False):
		vals = effects.getParticleAttr(self.__shapeName, at=attributeName, array=True)
		if float3Array:
			vals = unflattenFloat3Array(vals)

		self.__data[attributeName] = dict(zip(self.__ids, vals))

	def getAttribute(self, pid, name):
		return self.__data[name][pid]

	def findByProximity(self, pid, radius):
		pos = self.getAttribute(pid, "position")

		results = {}
		for k,v in self.__data["position"].iteritems():
			if inRadius(pos, v, radius):
				results[k] = v

		return results

def test(pid, shape):
	blah = ParticlesFrameData(shape)

	blah.loadAttribute("position", float3Array=True)

	return vectorAverage([v for k,v in blah.findByProximity(pid, 0.25).iteritems()])
