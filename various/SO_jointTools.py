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
How to compute the length of a joint chain.

Choose the start and end of a joint chain and run:
	
	import SO_jointTools
	SO_jointTools.computeLength(j1, j2)

"""

import pymel.core as pm

def computeLength(joint1, joint2):
	"""Computes the length between joint1 and joint2, where joint1 is a parent of
	joint2.

	The function will travel up the whole joint chain, and will work with any child
	of joint1.
	"""

	joint1, joint2 = pm.PyNode(joint1), pm.PyNode(joint2)

	if (not joint1 or not joint2) or \
		(joint1.nodeType() != "joint" or joint2.nodeType() != "joint"):
		raise TypeError("One of the provided values is not a joint node.")
	
	if not joint1.isParentOf(joint2):
		raise ValueError("joint1 is not a parent of joint2.")

	# We could do integration here, treat the joints as a curve,
	# but lets keep it simple and just check the magnitudes for
	# all the vectors.

	total_mag = 0.0
	curr = joint2
	while curr != joint1:
		p = pm.listRelatives(curr, parent=True)[0]
		total_mag += (curr.getTranslation(space="world") - p.getTranslation(space="world")).length()
		curr = p

	return total_mag