# Copyright (c) 2017, Dr. Edmund Weitz

# simple geometry library to use from within Jupyter

# for educational purposes only, without any error checking or
# optimizations; not recommended for production use

from matrices import Matrix
from vectors import Vector
from IPython.display import display, clear_output, Javascript
from math import cos, sin, atan2, pi

class Canvas (object):
    canvasCounter = 0

    def __init__ (self, size = 200):
        self.SIZE = size
        self.POINT_RADIUS = 1 if self.SIZE < 400 else 2
        self.LINE_WIDTH = 1 if self.SIZE < 400 else 2
        self.ARROW_SIZE = 6 if self.SIZE < 400 else 8
        self.TRANSFORM = Matrix([[self.SIZE / 20, 0], [0, -self.SIZE / 20]])
        self.SHIFT = Vector(self.SIZE / 2, self.SIZE / 2)
        Canvas.canvasCounter += 1
        self.canvasID = "canvas_{}".format(Canvas.canvasCounter)
        display(Javascript("""
element.append("<canvas id='{}' width={} height={} style='background-color: #f0f0f0'></canvas>")
""".format(self.canvasID, self.SIZE, self.SIZE)))

    def _toCanvas (self, coords):
        return self.TRANSFORM * Vector(coords) + self.SHIFT

    def _JS (self, code):
        clear_output()
        display(Javascript("""
var context = document.getElementById('{}').getContext("2d")
{}
""".format(self.canvasID, code)))

    def clear (self):
        self._JS("context.clearRect(0, 0, {}, {})".format(self.SIZE, self.SIZE))

    def drawScreenPoint (self, coords, color = "black", radius = None):
        if not radius:
            radius = self.POINT_RADIUS
        self._JS("""
context.fillStyle = '{}'
context.beginPath()
context.arc({}, {}, {}, 0, 2 * Math.PI, false)
context.fill()
""".format(color, *coords, radius))

    def drawPoint (self, coords, color = "black", radius = None):
        self.drawScreenPoint(self._toCanvas(coords), color = color, radius = radius)

    def drawScreenCircle (self, center, radius, color = "black", width = None):
        if not width:
            width = self.LINE_WIDTH
        self._JS("""
context.lineWidth = {}
context.strokeStyle = '{}'
context.beginPath()
context.arc({}, {}, {}, 0, 2 * Math.PI, false)
context.stroke()
""".format(width, color, *center, radius))

    def drawCircle (self, center, radius, color = "black", width = None):
        self.drawScreenCircle(self._toCanvas(center),
                              (self._toCanvas((radius, 0)) - self._toCanvas((0,0))).norm(),
                              color = color, width = width)

    def drawScreenSegment (self, start, end, color = "black", width = None):
        if not width:
            width = self.LINE_WIDTH
        self._JS("""
context.lineWidth = {}
context.strokeStyle = '{}'
context.beginPath()
context.moveTo({}, {})
context.lineTo({}, {})
context.stroke()
""".format(width, color, *start, *end))

    def drawSegment (self, start, end, color = "black", width = None):
        self.drawScreenSegment(self._toCanvas(start), self._toCanvas(end), color = color, width = width)

    def drawScreenVector (self, end, start = (0,0), color = "black", width = None, arrowSize = None):
        if not width:
            width = self.LINE_WIDTH
        if not arrowSize:
            arrowSize = self.ARROW_SIZE
        self.drawScreenSegment(start, end, color = color, width = width)
        angle = atan2(end[1] - start[1], end[0] - start[0])
        self._JS("""
context.fillStyle = '{}'
context.beginPath()
context.moveTo({}, {})
context.lineTo({}, {})
context.lineTo({}, {})
context.closePath()
context.fill()""".format(color, *end,
                         end[0] + arrowSize * cos(pi + angle + 0.4),
                         end[1] + arrowSize * sin(pi + angle + 0.4),
                         end[0] + arrowSize * cos(pi + angle - 0.4),
                         end[1] + arrowSize * sin(pi + angle - 0.4)))

    def drawVector (self, end, start = (0,0), color = "black", width = None):
        self.drawScreenVector(self._toCanvas(end), self._toCanvas(start), color = color, width = width)

    def _extendScreenSegment (self, start, end):
        x1 = start[0]
        x2 = end[0]
        y1 = start[1]
        y2 = end[1]
        if x1 != x2:
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            return Vector(0, b), Vector(self.SIZE, m * self.SIZE + b)
        elif y1 != y2:
            m = (x2 - x1) / (y2 - y1)
            b = x1 - m * y1
            return Vector(b, 0), Vector(m * self.SIZE + b, self.SIZE)
        else:
            return None, None

    def drawScreenLine (self, p1, p2, color = "black", width = None):
        start, end = self._extendScreenSegment(p1, p2)
        if start:
            self.drawScreenSegment(start, end, color = color, width = width)

    def drawLine (self, p1, p2, color = "black", width = None):
        self.drawScreenLine(self._toCanvas(p1), self._toCanvas(p2), color = color, width = width)

    def drawScreenAxes (self, e1, e2, start, colors = ["#d0d0d0", "#ff4040", "#40ff40"],
                        width = None, vectors = True):
        if not width:
            width = self.LINE_WIDTH / 2
        self.drawScreenLine(start, e1, color = colors[0], width = width)
        self.drawScreenLine(start, e2, color = colors[0], width = width)
        if vectors:
            self.drawScreenVector(e1, start = start, color = colors[1], width = width)
            self.drawScreenVector(e2, start = start, color = colors[2], width = width)

    def drawAxes (self, e1 = (1,0), e2 = (0,1), start = (0,0),
                  colors = ["#d0d0d0", "#ff4040", "#40ff40"], width = None, vectors = True):
        self.drawScreenAxes(self._toCanvas(e1), self._toCanvas(e2), self._toCanvas(start),
                            colors = colors, width = width, vectors = vectors)

    def drawScreenGrid (self, e1, e2, start, range1 = [-25, 25], range2 = [-25, 25],
                        color = "#d0d0d0", width = None):
        if not width:
            width = self.LINE_WIDTH / 3
        start = Vector(start)
        e1 = Vector(e1) - start
        e2 = Vector(e2) - start
        for i in range(*range1):
            s = start + i * e2
            self.drawScreenLine(s, s + e1, color = color, width = width if i != 0 else width * 3)
        for i in range(*range2):
            s = start + i * e1
            self.drawScreenLine(s, s + e2, color = color, width = width if i != 0 else width * 3)

    def drawGrid (self, e1 = (1,0), e2 = (0,1), start = (0,0), range1 = [-10, 11], range2 = [-10, 11],
                  color = "#d0d0d0", width = None):
        self.drawScreenGrid(self._toCanvas(e1), self._toCanvas(e2), self._toCanvas(start),
                            color = color, width = width)

    def fillPolygon (self, L, color = "gray"):
        self._JS("""
context.fillStyle = '{}'
context.beginPath()
context.moveTo({}, {})
""".format(color, *self._toCanvas(L[0])))
        for P in L[1:]:
            self._JS("""
context.lineTo({}, {})
""".format(*self._toCanvas(P)))
        self._JS("""
context.closePath()
context.fill()
""")

    def fillCircle (self, center, radius, color = "gray"):
        radius = (self._toCanvas((radius, 0)) - self._toCanvas((0,0))).norm()
        self._JS("""
context.fillStyle = '{}'
context.beginPath()
context.arc({}, {}, {}, 0, 2 * Math.PI, false)
context.fill()
""".format(color, *self._toCanvas(center), radius))
