from tensor import *
from observedDistribution import *

def squareCompatibility(pattern):
    Pobs = observedDistr(pattern)
    Pa = Pobs.marginal1([0])
    Pb = Pobs.marginal1([1])
    Pc = Pobs.marginal1([2])
    Pd = Pobs.marginal1([3])
    Pac = Pobs.marginal2([0,2])
    Pbd = Pobs.marginal2([1,3])

    ans1 = True
    ans2 = True

    for x in [0, 1]:
        for y in [0, 1]:
            if Pac[x][y] != Pa[x] and Pc[y]:
                ans1 = False
            if Pbd[x][y] != Pb[x] and Pd[y]:
                ans2 = False

    ans = ans1 and ans2
    return ans
