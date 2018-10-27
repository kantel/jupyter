# Copyright (c) 2017-2018, Dr. Edmund Weitz

# simple layer atop matplotlib to facilitate drawing of functions,
# curves, and surfaces; intended for educational purposes and without
# any error checking or optimizations; not recommended for production
# use

# partially explained in this video (in German):
# https://youtu.be/BhtnlKOC-0s?list=PLb0zKSynM2PBYzz6l37rWH3B_n_7P40QP

# plotFunc2D: draw a function which maps reals to reals; first
# argument is the function (or a list of several functions), second
# argument is a two-element list denoting an interval which is the
# domain of the function to be plotted; optional arguments are "range"
# ("clip" interval for function values), "samples" (number of
# intermediate points computed), "scaled" (whether both axes should
# have the same scale), and "grid" (whether a grid should be shown)

# instead of functions, plotFunc2D also accepts lists of "points"
# (two-element lists or two-element tuples) for which a scatter plot
# will be shown; this can be useful if you are investigating
# interpolations

# plotCurve2D: draw a parametrized curve in the plane; first argument
# is a unary function returning pairs (or a list of such functions);
# accepts optional "range", "scaled" and "samples" arguments like
# above; "xRange" and "yRange" can also be specified separately

# plotFunc3D: similar to plotFunc2D but for functions which map pairs
# of real numbers to reals

# plotCurve3D: similar to plotCurve2D but for curves in space

# plotSurface3D: similar to plotCurve3D but for surfaces parametrized
# by two parameters

# plotContour: creates a contour plot of a function which maps pairs
# of reals to reals

# plotVectorField2D: for functions which map two reals to a pair of
# reals

# plotSlopeField: for drawing the slope field of an ordinary
# differential equation of order 1; first argument should map an (x,y)
# pair to the tangent slope

# plotVectorField3D: for functions which map three reals to a triple
# of reals

# plotComplexAbs, plotComplexReal, plotComplexImag: similar to
# plotFunc3D, but for functions which map complex numbers to complex
# numbers; only the absolute value of the function, the real part, or
# the imaginary part is visualized

# plotComplexContourAbs, plotComplexContourReal,
# plotComplexContourImag: similar to plotContour, but for functions
# which map complex numbers to complex numbers; only the absolute
# value of the function, the real part, or the imaginary part is
# visualized


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from itertools import chain
from math import nan, sqrt

def getPlotSize ():
    return plt.rcParams["figure.figsize"]

def setPlotSize (x, y):
    plt.rcParams["figure.figsize"] = [x, y]

def plotFunc2D (F, domain, range = None, samples = 100, scaled = False, grid = False):
    if callable(F):
        F = [F]
    if type(F) is list and ((type(F[0]) is list and not (type(F[0][0]) is list or type(F[0][0]) is tuple)) or type(F[0]) is tuple):
        F = [F]
    for f in F:
        if callable(f):
            X = np.linspace(*domain, samples)
            Y = np.fromiter((f(x) for x in X), np.float, samples)
            plt.plot(X, Y)
        else:
            plt.scatter([p[0] for p in f], [p[1] for p in f], marker = 'o', c = 'red')
    plt.margins(0.05, 0.1)
    if scaled:
        plt.axis("scaled")
    plt.grid(grid)
    if range:
        plt.ylim(range)

def plotCurve2D (F, domain, range = None, xRange = None, yRange = None, samples = 100, scaled = False):
    if callable(F):
        F = [F]
    for f in F:
        T = np.linspace(*domain, samples)
        V = np.fromiter(chain.from_iterable(f(t) for t in T), np.float, 2 * samples)
        plt.plot(V[::2], V[1::2])
    plt.margins(0.05, 0.1)
    if scaled:
        plt.axis("scaled")
    if range:
        if not xRange:
            xRange = range
        if not yRange:
            yRange = range
    if xRange:
        plt.xlim(xRange)
    if yRange:
        plt.ylim(yRange)

colorMaps = [cm.Greys, cm.Purples, cm.Greens, cm.Oranges, cm.Blues, cm.Reds]

def plotFunc3D (F, xDomain, yDomain = None, range = None, samples = 40, xSamples = None, ySamples = None, lines = True, labels = ['x', 'y', 'f(x,y)']):
    if callable(F):
        F = [F]
    if not xSamples:
        xSamples = samples
    if not ySamples:
        ySamples = samples
    if not yDomain:
        yDomain = xDomain
    X = np.linspace(*xDomain, xSamples) 
    Y = np.linspace(*yDomain, ySamples)
    X, Y = np.meshgrid(X, Y)
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_zlabel(labels[2])
    i = 0
    for f in F:
        if range:
            def g (x, y):
                val = f(x,y)
                return val if range[0] <= val <= range[1] else nan
        else:
            g = f
        Z = np.vectorize(g)(X, Y)
        vmin = range[0] if range else None
        vmax = range[1] if range else None
        ax.plot_surface(X, Y, Z, cmap = colorMaps[i % len(colorMaps)], vmin = vmin, vmax = vmax, rstride = 1, cstride = 1, linewidth = None if lines else 0, antialiased = lines)
        i += 1
    ax.margins(0.05, 0.05, 0.05)
    if range:
        ax.set_zlim(*range)
    plt.margins(0.05, 0.1)

def plotContour (f, xDomain, yDomain = None, range = None, samples = 100, xSamples = None, ySamples = None, scaled = None, labels = True):
    if not xSamples:
        xSamples = samples
    if not ySamples:
        ySamples = samples
    if not yDomain:
        yDomain = xDomain
    X = np.linspace(*xDomain, xSamples) 
    Y = np.linspace(*yDomain, ySamples)
    X, Y = np.meshgrid(X, Y)
    Z = np.vectorize(f)(X, Y)
    P = plt.contour(X, Y, Z)
    if labels:
        plt.clabel(P, inline = 1, fontsize = 10)
    if scaled:
        plt.axis("scaled")

def plotVectorField2D (f, xDomain, yDomain = None, range = None, samples = 20, xSamples = None, ySamples = None, scaled = None, angles = "uv"):
    if not xSamples:
        xSamples = samples
    if not ySamples:
        ySamples = samples
    if not yDomain:
        yDomain = xDomain
    X = np.linspace(*xDomain, xSamples) 
    Y = np.linspace(*yDomain, ySamples)
    X, Y = np.meshgrid(X, Y)
    U, V = np.vectorize(f)(X, Y)
    plt.quiver(X, Y, U, V, angles = angles)
    if scaled:
        plt.axis("scaled")

def plotSlopeField (f, xDomain, yDomain = None, range = None, samples = 20, xSamples = None, ySamples = None, scaled = None):
    def F (x, y):
        u = 1
        v = f(x, y)
        n = sqrt(u * u + v * v)
        return (u / n, v / n)
    plotVectorField2D(F, xDomain, yDomain = yDomain, range = range,
                         samples = samples, xSamples = xSamples, ySamples = ySamples, scaled = scaled, angles = "xy")

def plotVectorField3D (f, xDomain, yDomain = None, zDomain = None, range = None, samples = 5, xSamples = None, ySamples = None, zSamples = None):
    if not xSamples:
        xSamples = samples
    if not ySamples:
        ySamples = samples
    if not zSamples:
        zSamples = samples
    if not yDomain:
        yDomain = xDomain
    if not zDomain:
        zDomain = xDomain
    X = np.linspace(*xDomain, xSamples)
    Y = np.linspace(*yDomain, ySamples)
    Z = np.linspace(*zDomain, zSamples)
    X, Y, Z = np.meshgrid(X, Y, Z)
    U, V, W = np.vectorize(f)(X, Y, Z)
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.quiver(X, Y, Z, U, V, W)

def plotCurve3D (F, domain, samples = 100, range = None, xRange = None, yRange = None, zRange = None):
    if callable(F):
        F = [F]
    T = np.linspace(*domain, samples)
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    for f in F:
        V = np.fromiter(chain.from_iterable(f(t) for t in T), np.float, 3 * samples)
        ax.plot(V[::3], V[1::3], V[2::3])
    if range:
        if not xRange:
            xRange = range
        if not yRange:
            yRange = range
        if not zRange:
            zRange = range
    if xRange:
        ax.set_xlim(*xRange)
    if yRange:
        ax.set_ylim(*yRange)
    if zRange:
        ax.set_zlim(*zRange)
    ax.margins(0.05, 0.05, 0.05)

def plotSurface3D (f, xDomain, yDomain = None, samples = 50, xSamples = None, ySamples = None, range = None, xRange = None, yRange = None, zRange = None, lines = True):
    if not xSamples:
        xSamples = samples
    if not ySamples:
        ySamples = samples
    if not yDomain:
        yDomain = xDomain
    X = np.linspace(*xDomain, xSamples)
    Y = np.linspace(*yDomain, ySamples)
    X, Y = np.meshgrid(X, Y)
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    U, V, W = np.vectorize(lambda x, y: tuple(f(x,y)))(X, Y)
    if range:
        if not xRange:
            xRange = range
        if not yRange:
            yRange = range
        if not zRange:
            zRange = range
    if xRange:
        ax.set_xlim(*xRange)
    if yRange:
        ax.set_ylim(*yRange)
    if zRange:
        ax.set_zlim(*zRange)
    ax.plot_surface(U, V, W, cmap = cm.jet, rstride = 1, cstride = 1, linewidth = None if lines else 0, antialiased = lines)
    ax.margins(0.05, 0.05, 0.05)

def convertFuncs (F, conv):
    if callable(F):
        F = [F]
    return [conv(f) for f in F]

def plotComplexAbs (F, xDomain, yDomain = None, range = None, samples = 40, xSamples = None, ySamples = None, lines = True):
    plotFunc3D(convertFuncs(F, lambda f: lambda x, y: abs(f(complex(x, y)))), xDomain, yDomain = yDomain, range = range, samples = samples, xSamples = xSamples, ySamples = ySamples, lines = lines, labels = ['Re(z)', 'Im(z)', 'Abs(f(z))'])

def plotComplexReal (F, xDomain, yDomain = None, range = None, samples = 40, xSamples = None, ySamples = None, lines = True):
    plotFunc3D(convertFuncs(F, lambda f: lambda x, y: f(complex(x, y)).real), xDomain, yDomain = yDomain, range = range, samples = samples, xSamples = xSamples, ySamples = ySamples, lines = lines, labels = ['Re(z)', 'Im(z)', 'Re(f(z))'])

def plotComplexImag (F, xDomain, yDomain = None, range = None, samples = 40, xSamples = None, ySamples = None, lines = True):
    plotFunc3D(convertFuncs(F, lambda f: lambda x, y: f(complex(x, y)).imag), xDomain, yDomain = yDomain, range = range, samples = samples, xSamples = xSamples, ySamples = ySamples, lines = lines, labels = ['Re(z)', 'Im(z)', 'Im(f(z))'])

def plotComplexCountourAbs (f, xDomain, yDomain = None, range = None, samples = 100, xSamples = None, ySamples = None, scaled = None, labels = True):
    plotContour(lambda x, y: abs(f(complex(x, y))), xDomain, yDomain = yDomain, range = range, samples = samples, xSamples = xSamples, ySamples = ySamples, scaled = scaled, labels = labels)

def plotComplexCountourReal (f, xDomain, yDomain = None, range = None, samples = 100, xSamples = None, ySamples = None, scaled = None, labels = True):
    plotContour(lambda x, y: f(complex(x, y)).real, xDomain, yDomain = yDomain, range = range, samples = samples, xSamples = xSamples, ySamples = ySamples, scaled = scaled, labels = labels)

def plotComplexCountourImag (f, xDomain, yDomain = None, range = None, samples = 100, xSamples = None, ySamples = None, scaled = None, labels = True):
    plotContour(lambda x, y: f(complex(x, y)).imag, xDomain, yDomain = yDomain, range = range, samples = samples, xSamples = xSamples, ySamples = ySamples, scaled = scaled, labels = labels)
