import sys
sys.path.insert(0, 'local_model')
import localDecomp
sys.path.insert(0, 'inflations')
import ring6, spiral
from z3 import *
import numpy as np
import csv

f = open('data/orbit.csv')
r = csv.reader(f)
orbit = []
for row in r:
    orbit.append([int(i) for i in row])
# Locality condition
satLocality = []
unsatLocality = []
for p in orbit:
    state = localDecomp.solve(p, 6)
    if state == sat:
        satLocality.append(p)
    else:
        unsatLocality.append(p)

print('Sat locality condition:', len(satLocality), '/', len(orbit))
print('Unsat locality condition:', len(unsatLocality), '/', len(orbit))
with open('data/satLocality.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(satLocality)
f.close()
with open('data/unsatLocality.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(unsatLocality)
f.close()

# Hexagon inflation
satRing6 = []
unsatRing6 = []
for p in unsatLocality:
    state = ring6.solve(p)
    if state == sat:
        satRing6.append(p)
    else:
        unsatRing6.append(p)
print('Sat hexagon inflation:', len(satRing6), '/', len(unsatLocality))
print('Unsat hexagon inflation:', len(unsatRing6), '/', len(unsatLocality))
with open('data/satRing6.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(satRing6)
f.close()
with open('data/unsatRing6.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(unsatRing6)
f.close()

# Spiral inflation
satSpiral = []
unsatSpiral = []
for p in satRing6:
    state = spiral.solve(p)
    if state == sat:
        satSpiral.append(p)
    else:
        unsatSpiral.append(p)
print('Sat spiral:', len(satSpiral), '/', len(unsatRing6))
print('Unsat spiral:', len(unsatSpiral), '/', len(unsatRing6))
with open('data/satSpiral.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(satSpiral)
f.close()
with open('data/unsatSpiral.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(unsatSpiral)
f.close()
