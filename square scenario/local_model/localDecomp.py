from z3 import *
from tensor import *

B = BoolSort()
Z = IntSort()

def responseFunc(inter, C):
    p = []
    count = 0
    for output in [0, 1]:
        inter1 = []
        for lhv1 in range(C):
            inter2 = []
            for lhv2 in range(C):
                inter2.append(inter[count])
                count = count+1
            inter1.append(inter2)
        p.append(inter1)
    return p

def solve(pattern, C):
    P = tensor(pattern)
    s = Solver()
    Pa = responseFunc(BoolVector('pA', 2*C**2), C)
    Pb = responseFunc(BoolVector('pB', 2*C**2), C)
    Pc = responseFunc(BoolVector('pC', 2*C**2), C)
    Pd = responseFunc(BoolVector('pD', 2*C**2), C)
    for delta in range(C):
        for alpha in range(C):
            s.add(Or(Pa[0][delta][alpha], Pa[1][delta][alpha]))
    for alpha in range(C):
        for beta in range(C):
            s.add(Or(Pb[0][alpha][beta], Pb[1][alpha][beta]))
    for beta in range(C):
        for gamma in range(C):
            s.add(Or(Pc[0][beta][gamma], Pc[1][beta][gamma]))
    for gamma in range(C):
        for delta in range(C):
            s.add(Or(Pd[0][gamma][delta], Pd[1][gamma][delta]))

    for a in [0, 1]:
        for b in [0, 1]:
            for c in [0, 1]:
                for d in [0, 1]:
                    Pabcd = Or([And(Pa[a][delta][alpha], Pb[b][alpha][beta],\
                    Pc[c][beta][gamma], Pd[d][gamma][delta])\
                    for alpha in range(C) for beta in range(C)\
                    for gamma in range(C) for delta in range(C)])

                    if P[a][b][c][d]:
                        s.add(Pabcd)
                    else:
                        s.add(Not(Pabcd))

    return s.check()
