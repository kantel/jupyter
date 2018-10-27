# Copyright (c) 2017, Dr. Edmund Weitz

# simple library for educational purposes without any error checking
# or optimizations; not recommended for production use

from matrices import Matrix
from vectors import Vector
from math import cos, sin

# returns a homogeneous matrix for scaling (with individual scaling
# factors for the x, y, and z directions)
def scalingMatrix (sx, sy, sz):
  return Matrix([[sx, 0, 0, 0],
                 [0, sy, 0, 0],
                 [0, 0, sz, 0],
                 [0, 0, 0, 1]])

# returns a homogeneous matrix for a translation along the
# vector (x, y, z) - or along x if x is itself a vector
def translationMatrix (x, y = 0, z = 0):
  if type(x) is Vector:
    y = x[1]
    z = x[2]
    x = x[0]
  return Matrix([[1, 0, 0, x],
                 [0, 1, 0, y],
                 [0, 0, 1, z],
                 [0, 0, 0, 1]])

# returns a homogeneous matrix for a rotation about the x axis
def xRotationMatrix (angle):
  return Matrix([[1, 0, 0, 0],
                 [0, cos(angle), -sin(angle), 0],
                 [0, sin(angle), cos(angle), 0],
                 [0, 0, 0, 1]])

# returns a homogeneous matrix for a rotation about the y axis
def yRotationMatrix (angle):
  return Matrix([[cos(angle), 0, sin(angle), 0],
                 [0, 1, 0, 0],
                 [-sin(angle), 0, cos(angle), 0],
                 [0, 0, 0, 1]])

# returns a homogeneous matrix for a rotation about the z axis
def zRotationMatrix (angle):
  return Matrix([[cos(angle), -sin(angle), 0, 0],
                 [sin(angle), cos(angle), 0, 0],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]])

# returns the homogeneous equivalent of a 3-dimensional vector
def lift (vec):
    return Vector(vec[0], vec[1], vec[2], 1)

# returns 3-dimensional equivalent of a homogeneous vector
def lower (vec):
    return Vector(vec[0] / vec[3], vec[1] / vec[3], vec[2] / vec[3])
