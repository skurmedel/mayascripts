# Simon Otter 2012.

# This script isn't finished bro. So, you know, bro; check it out later.

import pymel.core as pm


def attachInstance(source, target, p):
    """Instances source, and attaches it to mesh target as close
    as it can on the surface to point p."""
    
    n = pm.PyNode(target)
    if n.nodeType() == "transform" and n.numChildren():
    	n = n.getChildren()[0]
    if n.nodeType() != "mesh":
    	raise ValueError("target must point to a polygon mesh.")

    inst = pm.instance(source)
    constraint = pm.pointOnPolyConstraint(target, inst)

    uvs = n.getUVAtPoint(p, space="world")

    transform = n.firstParent()

    constraint.attr("%sU0" % transform.nodeName()).set(uvs[0])
    constraint.attr("%sV0" % transform.nodeName()).set(uvs[1])

def raycastPosition():
	return pm.autoPlace(useMouse=True)