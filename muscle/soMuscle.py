import pymel.core as pm
import operator

class SoMuscle(object):
    def __init__(self, start, end, name="soMuscle"):
        """Defines a new muscle positioned between start and end.

        start & end must both be locators.

        The locators are hijacked by the muscle and moved into its own special group.

        :param start: A locator describing where the muscle starts.
        :param end:   A locator describing where the muscle ends.
        :param name:  (optional) A descriptive name for the muscle (group.)
        """
        snode = pm.PyNode(start)
        if snode is None:
            raise ValueError("Couldn't deduce Maya type for start.")
        enode = pm.PyNode(end)
        if enode is None:
            raise ValueError("Couldn't dedude Maya type for end.")

        def findshape(n):
            if n.nodeType() == "transform":
                children = n.getChildren() # Can probably use n.getShape() here.
                if len(children) > 0:
                    return children[0], n
                else:
                    raise TypeError("Expected a locator or its transform node in start")
            elif n.nodeType() == "locator":
                return n, n.getParent()
            else:
                    raise TypeError("Expected a locator or its transform node in start")

        snode, strans = findshape(snode)
        enode, etrans = findshape(enode)

        grp = pm.group(empty=True, name=name)
        strans.setParent(grp)
        etrans.setParent(grp)

        # Create start and end circle.
        positions = [x.getTranslation(space="world") for x in [strans, etrans]]
        rotations = [x.getRotation(space="world") for x in [strans, etrans]]
        positions.append(positions[0] + (positions[1] - positions[0]) * 0.5)
        rotations.append(rotations[1])
        circles = []
        for name, p, quat in zip(["start", "end", "mid"], positions, rotations):
            trans, makecircle = pm.circle(name=name, radius=0.25)
            trans.setTranslation(p)
            trans.setRotation(quat)
            circles.append(trans)

        for trans, parent in zip(circles, [strans, etrans, grp]):
            trans.setParent(parent)

        pm.loft(*circles)
