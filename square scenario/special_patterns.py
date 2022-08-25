import sys
import numpy as np
from z3 import *
from compatibility import *
sys.path.insert(0, 'inflations')
import ring8, ring12
from observedDistribution import *
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

# p_hardy
p_hardy = [1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1]
PR_box = [1,1,1,0,0,0,0,1,0,0,0,1,1,1,1,0]

def solve(pattern, C):
    P = tensor(pattern)
    s = Solver()
    Pa = responseFunc(BoolVector('pA', 2*C**2), C)
    Pb = responseFunc(BoolVector('pB', 2*C**2), C)
    Pc = responseFunc(BoolVector('pC', 2*C**2), C)
    Pd = responseFunc(BoolVector('pD', 2*C**2), C)
    for delta in range(2):
        for alpha in range(C):
            s.add(Or(Pa[0][delta][alpha], Pa[1][delta][alpha]))
    for alpha in range(C):
        for beta in range(2):
            s.add(Or(Pb[0][alpha][beta], Pb[1][alpha][beta]))
    for beta in range(2):
        for gamma in range(1):
            s.add(Or(Pc[0][beta][gamma], Pc[1][beta][gamma]))
    for gamma in range(1):
        for delta in range(2):
            s.add(Or(Pd[0][gamma][delta], Pd[1][gamma][delta]))

    for a in [0, 1]:
        for b in [0, 1]:
            for c in [0, 1]:
                for d in [0, 1]:
                    Pabcd = Or([And(Pa[a][delta][alpha], Pb[b][alpha][beta],\
                    Pc[c][beta][gamma], Pd[d][gamma][delta])\
                    for alpha in range(C) for beta in range(2)\
                    for gamma in range(1) for delta in range(2)])

                    if P[a][b][c][d]:
                        s.add(Pabcd)
                    else:
                        s.add(Not(Pabcd))

    return s.check()


# check nonlocality
print("Hardy")
for C in range(2,12+1):
    res = solve(p_hardy, C)
    print("C=",C," ", res)

print("PR-box")
for C in range(2,12+1):
    res = solve(PR_box, C)
    print("C=",C," ",res)

print(ring8.solve(p_hardy))
print(ring8.solve(PR_box))    
