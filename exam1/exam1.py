#!/usr/bin/env python3
#
# CME 211, Fall 2018
# Python Midterm Exam
#

# You can use some or all of these modules
import copy
import math
import sys
import time


class Vector:
    def __init__(self, size, val):
        self.__data=[val]*size
    def __len__(self):
        return len(self.__data)
    def get(self, i):
        return self.__data[i]
    def put(self, i, val):
        self.__data[i] = val

## Your code here ##

class Matrix:
    def importMatrix(self,filename):
        raise RuntimeError("Must use specific matrix type")
    def get(self,i,j):
        raise RuntimeError("Must use specific matrix type")
    def set(self,i,j,x):
        raise RuntimeError("Must use specific matrix type")
    def matvec(self,v):
        raise RuntimeError("Must use specific matrix type")
    def numCols(self):
        raise RuntimeError("Must use specific matrix type")

class DenseMatrix(Matrix):
    def __init__(self):
        self.__rows = 0
        self.__cols = 0
        self.__data = []

    def importMatrix(self,filename):
        with open(filename,'r') as f:
            readDimension = False
            for line in f:
                if line[0] == '%':
                    continue
                elif readDimension == False:
                    readDimension = True
                else:
                    entry = line.split()
                    i = int(entry[0])
                    j = int(entry[1])
                    x = float(entry[2])
                    self.set(i-1,j-1,x)
                
        
    def get(self,i,j):
        return self.__data[i][j]
        
    def set(self,i,j,x):
        while i >= self.__rows:
            self.__data.append([])
            self.__rows += 1
            for n in range(self.__cols):
                self.__data[self.__rows-1].append(0)
        while j >= self.__cols:
            for row in self.__data:
                row.append(0)
            self.__cols += 1
        self.__data[i][j] = x
            
        
    def matvec(self,v):
        ncols = self.numCols()
        if ncols != len(v):
            raise RuntimeError("Vector and matrix dimensions mismatched")
        result = Vector(ncols,0)
        for i in range(ncols):
            for j in range(ncols):
                x = result.get(i)
                addval = self.__data[i][j]*v.get(j)
                result.put(i,x + addval)
        return result
        
    def numCols(self):
        return self.__cols

class SparseMatrix(Matrix):
    def __init__(self):
        self.__values = []
        self.__colind = []
        self.__rowptr = []

    def importMatrix(self,filename):
        with open(filename,'r') as f:
            readDimension = False
            self.__values.clear()
            self.__colind.clear()
            self.__rowptr.clear()
            self.__rowptr.append(0)
            self.__rowptr.append(1)
            for line in f:
                if line[0] == '%':
                    continue
                elif readDimension == False:
                    readDimension = True
                else:
                    entry = line.split()
                    i = int(entry[0])
                    j = int(entry[1])
                    x = float(entry[2])
                    self.set(i-1,j-1,x)

    def get(self,i,j):
        rowStart = self.__rowptr[i]
        rowEnd = self.__rowptr[i+1]
        row = self.__values[rowStart:rowStop]
        rowCols = self.__colind[rowStart:rowStop]
        try:
            ind = rowCols.index(j)
            return row[ind]
        except ValueError:
            return 0

    def set(self,i,j,x):
        if i > len(self.__rowptr)+1:
            self.__values.append(x)
            self.__colind.append(j)
            last = self.__rowptr[-1]
            while len(self.__rowptr) <= i:
                self.__rowptr.append(last)
            self.__rowptr.append(last+1)
        else:        
            rowStart = self.__rowptr[i]
            rowEnd = self.__rowptr[i+1]
            try:
                ind = self.__colind.index(j,rowStart,rowEnd)
                self.__values[ind] = x
            except ValueError:
                rowCols = self.__colind[rowStart:rowEnd]
                rowCols.append(j)
                rowCols.sort()
                ind = rowStart + rowCols.index(j)
                self.__values.insert(ind,x)
                self.__colind.insert(ind,j)
                for a in range(i+1,len(self.__rowptr)):
                    self.__rowptr[a] += 1
            

    def matvec(self,v):
        ncols = self.numCols()
        if ncols != len(v):
            raise RuntimeError("Vector and matrix dimensions mismatched")
        result = Vector(ncols,0)
        for i in range(ncols):
            row = self.__values[self.__rowind[i]:self.__rowind[i+1]]
            rowCols = self.__colind[self.__rowind[i]:self.__rowind[i+1]]
            for n in range(len(row)):
                x = result.get(i)
                j = rowCols[n]
                addval = row[n] * v.get(j)
                result.put(i,x+addval)
        return result

    def numCols(self):
        return max(self.__colind)+1

    
def areEqual(u,v):
    length = u.len()
    if v.len() != length:
        raise RuntimeError("Vectors are of different length")
    for i in range(length):
        a = u.get(i)
        b = v.get(i)
        if math.isclose(a,b):
            continue
        else:
            return False
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage:')
        print('  python {} <matrix market file>'.format(sys.argv[0]))
        sys.exit(0)

    matrixdata = sys.argv[1]

    #
    # The code below this will not work until you implement
    # all `*Matrix` classes and `areEqual` function. You may comment
    # out portions of the code while you are developing and testing
    # your classes and the function. 
    #

    # Declare dense and sparse matrix
    M = DenseMatrix()
    S = SparseMatrix()

    # Load dense matrix
    M.importMatrix(matrixdata)
    for i in range(M.numCols()):
        for j in range(M.numCols()):
            print("({},{}) = {}".format(i,j,M.get(i,j)))

    # Load sparse matrix
    S.importMatrix(matrixdata)
    S.importMatrix(matrixdata)
    for i in range(S.numCols()):
        for j in range(S.numCols()):
            print("({},{}) = {}".format(i,j,S.get(i,j)))

    # Create vector for testing matvec method
    v = Vector(M.numCols(), 0.1)

    # Dense matrix-vector multiplication
    r = M.matvec(v)

    # Sparse matrix-vector multiplication
    q = S.matvec(v)

    # Verify sparse matrix vector multiplication against the dense one
    if areEqual(r,q):
        print("Sparse matvec verified!")
    else:
        print("Sparse matvec verification failed!")
