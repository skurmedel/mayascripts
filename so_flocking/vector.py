# Copyright (c) 2012, Simon Otter
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SIMON OTTER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Various functions that help with vector manipulation.

Most of the functions in this module requires the following interface:

    __add__     Two vectors, returns a vector.
    __sub__     - | | -
    __div__     A vector and a scalar, returns a vector.
    __mul__     A vector and a scalar, returns a vector.
    __len__     Magnitude of the vector. See mag for more information.

The operations themselves are just the corresponding vector operations,
addition, subtraction, division with a scalar, multiplication with a scalar.
"""
import __builtin__
from unittest import TestCase
import math
import itertools

# Gets the magnitude/length of a vector. Set this to a custom method if __len__ is not part
# of the vector interface.
mag = __builtin__.len

def avg(vectors):
    """
    Get the average vector for a list of vectors

    vectors is an iterable (preferably a list) who's members
    have a plus and division operator specified.
    """

    return reduce(lambda x, y: x + y, vectors) / len(vectors)

def inside(v, center, radius):
    """
    Finds out if a vector is inside a specific circle/sphere in space.
    """
    line = center - v

    return mag(line) <= radius

class Vector(object):
    """
    A simple 3D Vector type.
    """

    def __init__(self, *args):
        x, y, z = args

        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        """
        Vector addition.

        :rtype : Vector
        :type other: Vector
        """
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """
        Vector subtraction.

        :rtype : Vector
        :type other: Vector
        """
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __div__(self, other):
        """
        Division by scalar.

        :rtype : float
        :type other: float
        """
        return Vector(self.x / other, self.y / other, self.z / other)

    def __mul__(self, other):
        """
        Multiplication by scalar.

        :rtype : float
        :type other: float
        """
        return Vector(self.x * other, self.y * other, self.z * other)

    def __len__(self):
        """
        Magnitude of the vector.
        """
        return math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

    def __repr__(self):
        return "Vector(%f, %f, %f)" % (self.x, self.y, self.z)

class VectorsTest(TestCase):
    def test_avg(self):
        vectors = [Vector(x, y, z) for x in (0., 1.) for y in (0., 1.) for z in (0., 1.)]

        res = avg(vectors)
        self.assertAlmostEqual(0.5, res.x, 2)
        self.assertAlmostEqual(0.5, res.y, 2)
        self.assertAlmostEqual(0.5, res.z, 2)

    def test_inside(self):
        p = Vector(1, 0, 0)
        radius = 0.5
        v = Vector(0.25, 0, 0)

        self.assertTrue(inside(v, p, radius))