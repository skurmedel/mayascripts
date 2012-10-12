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
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pymel.core as pm
import pymel.core.datatypes as dt

def create(quads=True, it=1):
	name = pm.polyPlatonicSolid(n="geoSphere", st=1)
	for i in xrange(0, it):
		pm.polySmooth(name, mth=int(not quads), dv=1)

	vertices = pm.polyEvaluate(name, v=True)

	def make_vtxname(index):
		return str(name[0]) + ".vtx[" + str(index) + "]"

	for vtxname in (make_vtxname(vert) for vert in xrange(0, vertices)):
	    p = pm.xform(vtxname, q=True, t=True);
	    p = dt.Vector(p).normal()
	    
	    pm.move(p.x, p.y, p.z, vtxname)

def prompt_ui():
	win = pm.window(title="Create Geosphere", width=200)

	layout = pm.formLayout()

	rlayout = pm.rowLayout(parent=layout, numberOfColumns=2)
	iter_field_lbl = pm.text("Iterations", parent=rlayout)
	iter_field = pm.intField(min=1, max=5, step=1, v=1, parent=rlayout)

	quads_chbox = pm.checkBox(label="Create Quads?", v=False, parent=layout)

	def on_ok(*args):
		create(quads_chbox.getValue(), iter_field.getValue())
		win.delete()

	ok_button = pm.button(label="Create mah Geosphere!", command=on_ok, parent=layout)

	layout.redistribute()
	win.show()

prompt_ui()