from math import cos, sin, pi
from vectors import Vector

def arc (center, startAngle = 0, endAngle = 2 * pi,
         inc = 0.1, xScale = None, yScale = 1):
    if not xScale:
        xScale = 2 * yScale
    points = []
    t = startAngle
    while t < endAngle:
        points.append(center + Vector(xScale * cos(t),
                                      yScale * sin(t)))
        t += inc
    return points

def smileyPoints ():
    # Kopf
    smiley = arc(Vector(3, 2))
    # Mund
    smiley += arc(Vector(3, 1.8), yScale = 0.5, inc = 0.2,
                  startAngle = pi + 0.2,
                  endAngle = 2 * pi - 0.2)
    # ein Auge
    smiley += arc(Vector(2, 2.4), yScale = 0.1, inc = 0.6,
                  startAngle = pi + 0.2,
                  endAngle = 2 * pi - 0.2)
    # das andere Auge
    smiley += [Vector(x, 2.4) for x in [3.9, 4, 4.1]]
    return smiley

def drawPoints (c, L, color = "black"):
    for p in L:
        c.drawPoint(p, color = color)
