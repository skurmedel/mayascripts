import pymel.core as pm
import pymel.core.datatypes as dt

def create_geosphere(quads=True, it=1):
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
		create_geosphere(quads_chbox.getValue(), iter_field.getValue())
		win.delete()

	ok_button = pm.button(label="Create mah Geosphere!", command=on_ok, parent=layout)

	layout.redistribute()
	win.show()

prompt_ui()