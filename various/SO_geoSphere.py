import pymel.core as pm
import pymel.core.datatypes as dt

name = pm.polyPlatonicSolid(n="geoSphere", st=1)
pm.polySmooth(name, mth=1, dv=1)
pm.polySmooth(name, mth=1, dv=1)
pm.polySmooth(name, mth=1, dv=1)

vertices = pm.polyEvaluate(name, v=True)

for vert in range(0, vertices):
    vtxname = (str(name[0]) + ".vtx[" + str(vert) + "]")
    p = pm.xform(vtxname, q=True, t=True);
    p = dt.Vector(p).normal()
    
    pm.move(p.x, p.y, p.z, vtxname)