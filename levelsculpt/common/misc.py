from copy import deepcopy
import math

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

def pointInsideCircle(point:Vector2, circlePos:Vector2, circleRadius:float):
    return circlePos.distSq(point) < circleRadius ** 2

def pointOnLine(point:Vector2, lineStart:Vector2, lineEnd:Vector2, elipson=0.05):
    # Taken shamelessly from p5collide2d.js

    lineLen = lineStart.dist(lineEnd)
    return (point.dist(lineStart) + point.dist(lineEnd) >= lineLen - elipson and
        point.dist(lineStart) + point.dist(lineEnd) <= lineLen + elipson)

def lineIntersectsCircle(lineStart:Vector2, lineEnd:Vector2,
    circlePos:Vector2, circleRadius:float):
    
    # Taken shamelessly from p5.collide2d.js

    # Is either end INSIDE the circle?
    inside1 = pointInsideCircle(lineStart, circlePos, circleRadius)
    inside2 = pointInsideCircle(lineEnd, circlePos, circleRadius)
    if inside1 or inside2:
        return True

    lineLen = lineStart.dist(lineEnd)

    dot = (((circlePos.x - lineStart.x)*(lineEnd.x-lineStart.x)) +
        ((circlePos.y-lineStart.y)*(lineEnd.y-lineStart.y)) ) / lineLen ** 2

    closestPos = Vector2(
        lineStart.x + (dot * (lineEnd.x - lineStart.x)),
        lineStart.y + (dot * (lineEnd.y - lineStart.y)))

    if not pointOnLine(closestPos, lineStart, lineEnd):
        return False
    
    distToLine = closestPos.distSq(circlePos)
    return distToLine < circleRadius ** 2