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

"""A collection of modelling related stuff.

How to use?

Make sure Maya has sourced the script file. Any function can then be called by

	SO_modellingTools.funcName(params)

where funcName is the function name and params are standard Python parameters.

For example:
	
	SO_modellingTools.insertEdgeLoop(weight=0.25)

"""

import pymel.core as pm

def insertEdgeLoop(weight=0.5, sma=3, splitType=1, div=1):
	"""Mimics Insert Edge Loop in Maya, as it is 
	used in the UI, and not how it works in MEL.
	"""
	
	edges = pm.filterExpand(expand=True, sm=32)
	for e in edges:
		e = pm.PyNode(e)
		pm.select(e, r=True)
		pm.polySelect(er=e.currentItemIndex())
		pm.polySplitRing(weight=weight, fixQuads=1, splitType=splitType, sma=sma, div=div)