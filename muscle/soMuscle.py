import pymel.core as pm
import operator

class SoMuscle(object):
    def __init__(self, grpname):
        """Creates a new SoMuscle object representing the muscle hierarchy specified in grpname.

        grpname must point to a valid Maya group with the requisite structure.
        """
        raise NotImplemented("Coming soon.")

    @classmethod
    def make(cls, start, end, name="soMuscle"):
        """Creates a new muscle positioned between start and end.

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

        def getrottrans(trans):
            return trans.getRotation(space="world"), trans.getTranslation(space="world")

        # Find locator shapes, mostly to make sure they are locators.
        # Their transforms are needed though.
        snode, sloctrans = findshape(snode)
        enode, eloctrans = findshape(enode)

        mloctrans = pm.spaceLocator()
        # Point-constrain and orient constrain to other locators.
        pm.pointConstraint(sloctrans, eloctrans, mloctrans, maintainOffset=False)
        pm.orientConstraint(sloctrans, eloctrans, mloctrans)

        maingrp = pm.group(empty=True, name=name)
        maingrp.translate.lock(), maingrp.rotate.lock(), maingrp.scale.lock()

        grp = pm.group(empty=True, name="moveGroup")
        grp.setParent(maingrp)

        sloctrans.setParent(grp), sloctrans.rename("muscleStart")
        eloctrans.setParent(grp), eloctrans.rename("muscleEnd")
        mloctrans.setParent(grp), mloctrans.rename("muscleMid")

        # Make the locators smaller in the UI.
        for loctrans in [sloctrans, mloctrans, eloctrans]:
            loctrans.getShape().localScale.set(0.25, 0.25, 0.25)

        startdef = ("start", sloctrans) + getrottrans(sloctrans)
        enddef   = ("end", eloctrans) + getrottrans(eloctrans)
        middef   = ("mid", mloctrans) + getrottrans(mloctrans)

        circles = []
        for name, parent, rot, pos in [startdef, middef, enddef]:
            transform, _ = pm.circle(radius=0.1)
            pm.delete(transform, ch=True)
            circles.append(transform)
            transform.setParent(parent)
            # Change name AFTER we've parented them, so we can avoid naming collisions.
            transform.rename(name)
            transform.setRotation(rot)
            transform.setTranslation(pos, space="world")

        loftrans, _ = pm.loft(*circles)
        loftrans.setParent(maingrp) # Put in maingrp, so we avoid double transforms.
        loftrans.rename("muscleSurface")

        midcircle = circles[1]
        def addfloat3(obj, attrname):
            obj.addAttr(attrname, at="float3")
            for suffix in ["X", "Y", "Z"]:
                obj.addAttr(attrname + suffix, at="float", parent=attrname, k=True)

        addfloat3(midcircle, "startPos")
        addfloat3(midcircle, "endPos")
        maingrp.addAttr("bulgeFactor", at="float", defaultValue=1.0, minValue=0.01, maxValue=1000, k=True)

        sloctrans.translate >> midcircle.startPos
        eloctrans.translate >> midcircle.endPos

        # Some horrible MEL to preserve volume.
        expression = """
            vector $a = <<{0}.startPosX, {0}.startPosY, {0}.startPosZ>>;
            vector $b = <<{0}.endPosX,   {0}.endPosY,   {0}.endPosZ>>;

            float $len = `mag ($b - $a)`;
            $len += 0.0000001;
            float $f = {1}.bulgeFactor / $len;
            scaleX = $f;
            scaleY = $f;
        """.format(midcircle.name(), maingrp.name())

        pm.expression(o=midcircle, s=expression)