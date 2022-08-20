import sys
import numpy as np
from z3 import *
from compatibility import *
sys.path.insert(0, 'local_model')
import localDecomp
sys.path.insert(0, 'inflations')
import ring8, ring12, web
from tqdm import *
from time import *
import csv

f = open('data/orbit.csv')
r = csv.reader(f)
orbit = []
for row in r:
    orbit.append([int(i) for i in row])

# Square compatibility
squareCompatible = []
squareIncompatible = []
for p in tqdm(orbit, ncols=70):
    state = squareCompatibility(p)
    if state == True:
        squareCompatible.append(p)
    else:
        squareIncompatible.append(p)

print('Square compatible:', len(squareCompatible), '/', len(orbit))
print('Square incompatible:', len(squareIncompatible), '/', len(orbit))

with open('data/squareCompatible.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(squareCompatible)
f.close()
with open('data/squareIncompatible.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(squareIncompatible)
f.close()

# Locality condition (cardinality C up to 3)
satLocality23 = []
satLocality3 = []
unsatLocality = []
for p in tqdm(squareCompatible, ncols=70):
    state3 = localDecomp.solve(p, 3) # Check locality condition for cardinality C = 3
    if state3 == sat:
        state2 = localDecomp.solve(p, 2)
        if state2 == sat:
            satLocality23.append(p)
        else:
            satLocality3.append(p)
    else:
        unsatLocality.append(p)

print('Sat locality condition C=3 & C=2:', len(satLocality23), '/', len(squareCompatible))
print('Sat locality condition C=3:', len(satLocality3), '/', len(squareCompatible))

with open('data/satLocality23.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(satLocality23)
f.close()
with open('data/satLocality3.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(satLocality3)
f.close()
with open('data/unsatLocality.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(unsatLocality)
f.close()

# Ring-8 inflation
satRing8 = []
unsatRing8 = []
for p in tqdm(unsatLocality, ncols=70):
    state = ring8.solve(p)
    if state == sat:
        satRing8.append(p)
    else:
        unsatRing8.append(p)

print('Sat ring-8:', len(satRing8), '/', len(unsatLocality))
print('unsatRing-8:', len(unsatRing8), '/', len(unsatLocality))

with open('data/satRing8.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(satRing8)
f.close()
with open('data/unsatRing8.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(unsatRing8)
f.close()

# Ring-12 inflation
satRing12 = []
unsatRing12 = []
for p in tqdm(satRing8, ncols=70):
    state = ring12.solve(p)
    if state == sat:
        satRing12.append(p)
    else:
        unsatRing12.append(p)

print('Sat ring-12:', len(satRing12), '/', len(satRing8))
print('Unsat ring-12:', len(unsatRing12), '/', len(satRing8))

with open('data/satRing12.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(satRing12)
f.close()
with open('data/unsatRing12.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(unsatRing12)
f.close()

# Web inflation
satWeb = []
unsatWeb = []
for p in tqdm(satRing12, ncols=70):
    state = web.solve(p)
    if state == sat:
        satWeb.append(p)
    else:
        unsatWeb.append(p)

print('Sat web (unsorted):', len(satWeb), '/', len(satRing12))
print('Unsat web:', len(unsatWeb), '/', len(satRing12))

with open('data/satWeb.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(satWeb)
f.close()
with open('data/unsatWeb.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(unsatWeb)
f.close()
