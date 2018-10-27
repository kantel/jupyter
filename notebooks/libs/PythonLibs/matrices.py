# Copyright (c) 2017, Dr. Edmund Weitz

# simple matrix library for educational purposes without any error
# checking or optimizations; not recommended for production use

# to create a new Matrix object, call Matrix with a list of lists as
# in Matrix([[2, 3], [4, 5]]); all lists must have the same size
# (although the constructor won't warn you if they don't); the
# individual lists, like [2, 3], will become the rows of the matrix

# alternatively, you can construct a matrix with, say,
# Matrix([v1,v2,v3]) where v1 to v3 are vectors (see file vectors.py);
# they will become the columns of the matrix

# as another alternative, use something like Matrix([1, 2, 3]) as an
# abbreviation for Matrix([[1, 2, 3]]); finally, you can use Matrix(v)
# where v is a Vector object in order to create a matrix with one
# column

# Matrix objects are printed as lists of lists with an "M" in front

# you can read an individual component of a Matrix object M using the
# syntax M[2, 3]

# the method size returns a pair which is (m, n) for an m x n matrix

# the methods row and col return the corresponding row or column as a
# list of components; copy returns a matrix with the same size and
# components; you can also create a copy of M with Matrix(M)

# Matrix objects should be treated as if they were immutable;
# specifically, you should not alter the contents of their "arr"
# property

# matrices of the same size can be added or subtracted and you can
# also write -M to create the additive inverse of a matrix M

# to multiply a Matrix M with a scalar a you can write a * M and also
# M * a; furthermore, you can use M / a instead of (1 / a) * M

# to multiply to matrices M and N, use M * N; if the second factor is
# a Vector object, it will be treated like a one-column matrix and the
# result will be converted to a Vector object; note that we're not
# using the more fitting 'M @ N' as it currently doesn't work with
# Brython

# use M.transpose() to transpose the matrix M, M.determinant() for its
# determinant, and M.invert() for the inverse matrix (or None if it
# doesn't exist)

# the static methods zero and identity are for creating zero matrices
# and identity matrices of the corresponding sizes

from numbers import Number
import vectors
import copy

class Matrix (object):
    def __init__ (self, arg):
        if type(arg) is Matrix:
            self.arr = copy.deepcopy(arg.arr)
        elif type(arg) is list:
            if isinstance(arg[0], Number):
                self.arr = [copy.deepcopy(arg)]
            elif isinstance(arg[0], vectors.Vector):
                self.arr = [[v[i] for v in arg] for i in range(len(arg[0]))]
            else:
                self.arr = copy.deepcopy(arg)
        elif type(arg) is tuple or type(arg) is vectors.Vector:
            self.arr = [[c] for c in arg]

    def __getitem__(self, key):
        return self.arr[key[0]][key[1]]

    def __repr__ (self):
        return "M" + str(self.arr)

    def size (self):
        return len(self.arr), len(self.arr[0])

    def row (self, index):
        return self.arr[index]

    def col (self, index):
        return [r[index] for r in self.arr]

    def copy (self):
        return Matrix(self)

    def __mul__ (self, other):
        if type(other) is vectors.Vector:
            return vectors.Vector((self * Matrix(other)).col(0))
        elif type(other) is Matrix:
            return Matrix([[sum(a * b for a, b in zip(r, other.col(i)))
                            for i in range(other.size()[1])] for r in self.arr])
        else:
            return Matrix([list(other * c for c in r) for r in self.arr])

    def __rmul__ (self, other):
        return self.__mul__(other)
            
    def __truediv__ (self, other):
        return self.__mul__(1 / other)

    def __add__ (self, other):
        return Matrix([[a + b for a, b in zip(rS, rO)] for rS, rO in zip(self.arr, other.arr)])
    
    def __neg__ (self):
        return Matrix([[-a for a in r] for r in self.arr])

    def __sub__(self, other):
        return self + other.__neg__()
    
    def transpose (self):
        return Matrix([self.col(i) for i in range(self.size()[1])])

    @staticmethod
    def _gauss (A, B = None):
        A = Matrix(A)
        n = A.size()[0]
        A = A.arr
        if B:
            B = Matrix(B)
            p = B.size()[1]
            B = B.arr
        else:
            p = 0
        det = 1
        for i in range(n - 1):
            k = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[k][i]):
                    k = j
            if A[k][i] == 0:
                return 0, None
            if k != i:
                A[i], A[k] = A[k], A[i]
                if B:
                    B[i], B[k] = B[k], B[i]
                det = -det
            for j in range(i + 1, n):
                t = A[j][i] / A[i][i]
                for k in range(i + 1, n):
                    A[j][k] -= t * A[i][k]
                for k in range(p):
                    B[j][k] -= t * B[i][k]
        for i in range(n - 1, -1, -1):
            for j in range(i + 1, n):
                t = A[i][j]
                for k in range(p):
                    B[i][k] -= t * B[j][k]
            det *= A[i][i]
            if det == 0:
                return 0, None
            t = 1 / A[i][i]
            for j in range(p):
                B[i][j] *= t
        if B:
            B = Matrix(B)
        return det, B

    @staticmethod
    def zero (m, n = None):
        if n is None:
            n = m
        return Matrix([[0] * n for i in range(m)])

    @staticmethod
    def identity (n):
        I = Matrix.zero(n)
        for i in range(n):
            I.arr[i][i] = 1
        return I
       
    def determinant (self):
        return Matrix._gauss(self)[0]

    def invert (self):
        det, inv = Matrix._gauss(self, Matrix.identity(self.size()[0]))
        return inv if det != 0 else None
