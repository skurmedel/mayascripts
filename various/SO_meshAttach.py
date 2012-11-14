# Simon Otter 2012.

# This script isn't finished bro. So, you know, bro; check it out later.

import pymel.core as pm

def _getMeshNode(name):
    n = pm.PyNode(name)
    if n.nodeType() == "transform" and n.numChildren():
        n = n.getChildren()[0]
    if n.nodeType() != "mesh":
        raise ValueError("name must point to a polygon mesh.")
    return n

def attach(source, target, p):
    """Instances source, and attaches it to mesh target as close
    as it can on the surface to point p.
    """
    
    n = _getMeshNode(target)

    inst = pm.instance(source)
    constraint = pm.pointOnPolyConstraint(target, inst)

    uvs = n.getUVAtPoint(p, space="world")

    transform = n.firstParent()

    constraint.attr("%sU0" % transform.nodeName()).set(uvs[0])
    constraint.attr("%sV0" % transform.nodeName()).set(uvs[1])

def attachToVertices(source, targetVertices=None):
    """Instances source, and attaches each instance to each
    vertice.

    If targetVertices == None, the selected vertices are used.
    """

    if not targetVertices:
        targetVertices = pm.filterExpand(pm.ls(sl=True), expand=True, sm=31)
    else:
        if not hasattr("__next__", targetVertices):
            raise TypeError("targetVertices is not iterable.")

    for v in targetVertices:
        p = pm.pointPosition(v, w=True)

        target = pm.PyNode(v).node()

        attach(source, target, p)

def raycastPosition():
    return pm.autoPlace(useMouse=True)