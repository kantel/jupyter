# Copyright (c) 2017, Dr. Edmund Weitz

# simple vector library for educational purposes without any error
# checking or optimizations; not recommended for production use

# to create a new Vector object, call Vector with the components of
# the vector as arguments as in Vector(3, 4, 5)

# alternatively, use something like Vector([3, 4, 5]) or Vector((3, 4, 5)) to create vectors from lists or tuples;
# finally, you can use Vector(M) if M is a matrix
# (see file matrices.py) with only one column or only one row

# there's also a static method Vector.polar to create vectors from a
# length and an angle

# Vector objects are printed as tuples with a "v" in front

# you can read an individual component of a Vector object v using the
# syntax v[2]

# the method len returns the number of components

# copy returns a vector with the same components; you can also create
# a copy of v with Vector(v)

# Vector objects should be treated as if they were immutable;
# specifically, you should not alter the contents of their "comp"
# property

# vectors of the same length can be added or subtracted and you can
# also write -v to create the additive inverse of a vector v

# to multiply a vector v with a scalar a you can write a * v and also
# v * a; furthermore, you can use v / a instead of (1 / a) * v

# v.transpose() will return a one-row matrix with the vector's
# components

# v.norm() returns the Euclidean norm of the vector and v.normalize()
# returns v divided by its norm

# for the dot product of two vectors v and w, write v * w

# if you write v * M where M is a matrix, the result will be the
# product of two matrices where the first factor is the transposed
# vector; for M * v, see matrices.py

# vectors can be used as iterators; specifically, you can use *v if v
# is a Vector object

from math import sqrt, sin, cos
from numbers import Number
import matrices

class Vector (object):
    def __init__ (self, *args):
        if len(args) == 1:
            if type(args[0]) is tuple or type(args[0]) is list:
                self.comp = tuple(args[0])
            elif type(args[0]) is Vector:
                self.comp = args[0].comp
            elif type(args[0]) is matrices.Matrix:
                if args[0].size()[0] == 1:
                    self.comp = tuple(args[0].row(0))
                elif args[0].size()[1] == 1:
                    self.comp = tuple(args[0].col(0))
            elif isinstance(args[0], Number):
                self.comp = args
        else:
            self.comp = args

    def __iter__ (self):
        return self.comp.__iter__()
        
    def __repr__ (self):
        return "v" + str(self.comp)

    @staticmethod
    def polar (r, phi):
        return r * Vector(cos(phi), sin(phi))

    def copy (self):
        return Vector(self)

    def transpose (self):
        return matrices.Matrix([list(self)])

    def __mul__ (self, other):
        if type(other) is Vector:
            return sum(c * o for c, o in zip(self, other))
        elif type(other) is matrices.Matrix:
            return (self.transpose()) * other
        else:
            return Vector(*(other * c for c in self))
    
    def __rmul__ (self, other):
        return self.__mul__(other)

    def __mod__ (self, other):
        if len(self) == 3 and type(other) is Vector and len(other) == 3:
            return Vector(self[1] * other[2] - self[2] * other[1],
                          self[2] * other[0] - self[0] * other[2],
                          self[0] * other[1] - self[1] * other[0])

    def norm (self):
        return sqrt(self * self)
        
    def normalize (self):
        n = self.norm()
        if n == 0:
            return Vector([0] * len(self))
        else:
            return Vector(*(c / n for c in self))

    def __truediv__ (self, other):
        return self.__mul__(1 / other)
    
    def __add__ (self, other):
        return Vector(*(c + o for c, o in zip(self, other)))
    
    def __neg__ (self):
        return Vector(*(-c for c in self))

    def __sub__(self, other):
        return self + other.__neg__()
    
    def __len__(self):
        return len(self.comp)
    
    def __getitem__(self, key):
        return self.comp[key]
