from tensor import *
import numpy as np

class observedDistr:

    def __init__(self, pattern):
        inter = []

        for p in pattern:
            inter.append(bool(p))

        self.jointDistr = tensor(inter)
        self.vert = ['a', 'b', 'c']

    def marginal2(self, v):
        Pabc = self.jointDistr
        Pab = tensor([False for i in range(2**2)])
        Pac = tensor([False for i in range(2**2)])
        Pbc = tensor([False for i in range(2**2)])

        for x in [0, 1]:
            for y in [0, 1]:
                Pab[x][y] = Pabc[x][y][0] or Pabc[x][y][1]
                Pac[x][y] = Pabc[x][0][y] or Pabc[x][1][y]
                Pbc[x][y] = Pabc[0][x][y] or Pabc[1][x][y]

        if 0 in v and 1 in v:
            return Pab
        elif 0 in v and 2 in v:
            return Pac
        elif 1 in v and 2 in v:
            return Pbc

    def marginal1(self, v):
        Pa = [False, False]
        Pb = [False, False]
        Pc = [False, False]

        Pab = self.marginal2([0,1])
        Pac = self.marginal2([0,2])

        for x in [0, 1]:
            Pa[x] = Pab[x][0] or Pab[x][1]
            Pb[x] = Pab[0][x] or Pab[1][x]
            Pc[x] = Pac[0][x] or Pac[1][x]

        if 0 in v:
            return Pa
        elif 1 in v:
            return Pb
        elif 2 in v:
            return Pc

    def marginal(self, v):
        if len(v) == 3:
            return self.jointDistr
        elif len(v) == 2:
            return self.marginal2(v)
        elif len(v) == 1:
            return self.marginal1(v)
