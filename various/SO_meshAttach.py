# Simon Otter 2012.

# This script isn't finished bro. So, you know, bro; check it out later.

import pymel.core as pm


def attachInstance(source, target):
    """Instances source, and attaches it to mesh target."""
    
    # Rework this shit so it uses a parameter instead.
    vertices = pm.filterExpand(sm=31)
    
    for v in vertices:
        inst = pm.instance(source)
        constraint = pm.pointOnPolyConstraint(target, inst)   
    
        pos = pm.xform(v, q=True, t=True)
    
        n = pm.PyNode(target)
        uvs = n.getUVAtPoint(pos)
    
        constraint.attr("%sU0" % n.nodeName()).set(uvs[0])
        constraint.attr("%sV0" % n.nodeName()).set(uvs[1])