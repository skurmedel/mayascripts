import pymel.core as pm
import pymel.core.datatypes as dt

name = pm.polyPlatonicSolid(n="geoSphere", st=1)
pm.polySmooth(name, mth=1, dv=1)
pm.polySmooth(name, mth=1, dv=1)
pm.polySmooth(name, mth=1, dv=1)

vertices = pm.polyEvaluate(name, v=True)

def make_vtxname(index):
	return str(name[0]) + ".vtx[" + str(index) + "]"

for vtxname in (make_vtxname(vert) for vert in xrange(0, vertices)):
    p = pm.xform(vtxname, q=True, t=True);
    p = dt.Vector(p).normal()
    
    pm.move(p.x, p.y, p.z, vtxname)