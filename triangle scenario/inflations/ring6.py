from z3 import *
from tensor import *
from observedDistribution import *

B = BoolSort()
Z = IntSort()

def marginal4(k1, k2, k3, k4, v, P):
    w = []
    p = tensor([False for i in range(2**4)])

    for i in range(len(v)):
        if i != k1 and i != k2 and i != k3 and i != k4:
            w.append(i)

    for v[k1] in [0, 1]:
        for v[k2] in [0, 1]:
            for v[k3] in [0, 1]:
                for v[k4] in [0, 1]:
                    p[v[k1]][v[k2]][v[k3]][v[k4]] = Or([P[v[0]][v[1]][v[2]][v[3]][v[4]][v[5]]\
                    for v[w[0]] in [0, 1] for v[w[1]] in [0, 1]])

    return p

def marginal3(k1, k2, k3, v, P):
    w = []
    p = tensor([False for i in range(2**3)])

    for i in range(len(v)):
        if i != k1 and i != k2 and i != k3:
            w.append(i)

    for v[k1] in [0, 1]:
        for v[k2] in [0, 1]:
            for v[k3] in [0, 1]:
                p[v[k1]][v[k2]][v[k3]] = Or([P[v[0]][v[1]][v[2]][v[3]][v[4]][v[5]]\
                for v[w[0]] in [0, 1] for v[w[1]] in [0, 1] for v[w[2]] in [0, 1]])

    return p

def solve(pattern):
    s = Solver()
    a1, b1, c1, a2, b2, c2 = Ints('a1 b1 c1 a2 b2 c2')
    v = [a1, b1, c1, a2, b2, c2]
    Pobs = observedDistr(pattern)
    Pab = Pobs.marginal2([0,1])
    Pac = Pobs.marginal2([0,2])
    Pbc = Pobs.marginal2([1,2])
    Pa = Pobs.marginal1([0])
    Pb = Pobs.marginal1([1])
    Pc = Pobs.marginal1([2])

    p = Array('p', Z, B)
    inter = []
    for i in range(2**6):
        inter.append(Select(p, i))
    P = tensor(inter)

    Pa1b1a2b2 = marginal4(0,1,3,4,v,P)
    Pa1c2a2c1 = marginal4(0,5,3,2,v,P)
    Pb1c1b2c2 = marginal4(1,2,4,5,v,P)

    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for x3 in [0, 1]:
                for x4 in [0, 1]:
                    s.add(Pa1b1a2b2[x1][x2][x3][x4] == And(Pab[x1][x2], Pab[x3][x4]))
                    s.add(Pa1c2a2c1[x1][x2][x3][x4] == And(Pac[x1][x2], Pac[x3][x4]))
                    s.add(Pb1c1b2c2[x1][x2][x3][x4] == And(Pbc[x1][x2], Pbc[x3][x4]))

    Pa1b2c1 = marginal3(0,4,2,v,P)
    Pa2b1c2 = marginal3(3,1,5,v,P)

    for x1 in [0, 1]:
        for x2 in [0, 1]:
            s.add(Pa1b2c1[x1][x2][x3] == And(Pa[x1], Pb[x2], Pc[x3]))
            s.add(Pa2b1c2[x1][x2][x3] == And(Pa[x1], Pb[x2], Pc[x3]))

    return s.check()
