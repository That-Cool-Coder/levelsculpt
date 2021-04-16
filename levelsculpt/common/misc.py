from copy import deepcopy

from levelsculpt.common import Vector2

def defaultIfNone(checkValue, defaultValue, deepcopyDefault=True):
    # If checkValue is none, return defaultValue
    # else return checkValue
    # If deepcopyDefault is True then return a copy of defaultValue

    if checkValue is None:
        if deepcopyDefault:
            return deepcopy(defaultValue)
        else:
            return defaultValue
    else:
        return checkValue

def pointInsideRect(point:Vector2, rectTopLeft:Vector2, rectSize:Vector2):
    return point.x > rectTopLeft.x and \
        point.x < rectTopLeft.x + rectSize.x and \
        point.y > rectTopLeft.y and \
        point.y < rectTopLeft.y + rectSize.y