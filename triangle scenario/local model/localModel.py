from z3 import *
from tensor import *

B = BoolSort()
Z = IntSort()

def localDecomp(pattern, C):
    Pa = Function('Pa', Z, Z, Z, B)
    Pb = Function('Pb', Z, Z, Z, B)
    Pc = Function('Pc', Z, Z, Z, B)

    alpha, beta, gamma = Ints('alpha beta gamma')
    a, b, c = Ints('alpha beta gamma')

    P = tensor(pattern)
    s = Solver()

    for beta in range(C):
        for gamma in range(C):
            s.add(Or(Pa(0,beta,gamma), Pa(1,beta,gamma)))
    for gamma in range(C):
        for alpha in range(C):
            s.add(Or(Pb(0,gamma,alpha), Pb(1,gamma,alpha)))
    for alpha in range(C):
        for beta in range(C):
            s.add(Or(Pc(0,alpha,beta), Pc(1,alpha,beta)))

    for a in [0, 1]:
        for b in [0, 1]:
            for c in [0, 1]:
                Pabc = Or([And(Pa(a,beta,gamma), Pb(b,gamma,alpha), Pc(c,alpha,beta))\
                for alpha in range(C) for beta in range(C) for gamma in range(C)])

                if P[a][b][c]:
                    s.add(Pabc)
                else:
                    s.add(Not(Pabc))
    return s.check()
