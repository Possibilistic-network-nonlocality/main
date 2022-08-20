import numpy as np
from z3 import *
from observedDistribution import *
from compatibility import *
from localityCondition import *
from ring8 import *
from ring12 import *
from web import *
from tensor import *
from tqdm import *
from time import *

f = open('orbit.csv')
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

with open('squareCompatible.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(squareCompatible)
f.close()
with open('squareIncompatible.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(squareIncompatible)
f.close()

# Locality condition (cardinality C up to 3)
satLocality23 = []
satLocality3 = []
unsatLocality = []
for p in tqdm(squareCompatible, ncols=70):
    state3 = checkLocality(p, 3) # Check locality condition for cardinality C = 3
    if state3 == sat:
        state2 = checkLocality(p, 2)
        if state2 == sat:
            satLocality23.append(p)
        else:
            satLocality3.append(p)
    else:
        unsatLocality.append(p)

print('Sat locality condition C=3 & C=2:', len(satLocality23), '/', len(squareCompatible))
print('Sat locality condition C=3:', len(satLocality3), '/', len(squareCompatible))

with open('satLocality23.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(satLocality23)
f.close()
with open('satLocality3.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(satLocality3)
f.close()
with open('unsatLocality.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(unsatLocality)
f.close()

# Ring-8 inflation
satRing8 = []
unsatRing8 = []
for p in tqdm(unsatLocality, ncols=70):
    state = compatibilityRing8(p)
    if state == sat:
        satRing8.append(p)
    else:
        unsatRing8.append(p)

print('Sat ring-8:', len(satRing8), '/', len(unsatLocality))
print('unsatRing-8:', len(unsatRing8), '/', len(unsatLocality))

with open('satRing8.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(satRing8)
f.close()
with open('unsatRing8.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(unsatRing)
f.close()

# Ring-12 inflation
satRing12 = []
unsatRing12 = []
for p in tqdm(satRing8, ncols=70):
    state = compatibilityRing12(p)
    if state == sat:
        satRing12.append(p)
    else:
        unsatRing12.append(p)

print('Sat ring-12:', len(satRing12), '/', len(satRing8))
print('Unsat ring-12:', len(unsatRing12), '/', len(satRing8))

with open('satRing12.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(satRing12)
f.close()
with open('unsatRing12.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(unsatRing12)
f.close()

# Web inflation
satWeb = []
unsatWeb = []
for p in tqdm(satRing12, ncols=70):
    state = compatibilityWeb(p)
    if state == sat:
        satWeb.append(p)
    else:
        unsatWeb.append(p)

print('Sat web (unsorted):', len(satWeb), '/', len(satRing12))
print('Unsat web:', len(unsatWeb), '/', len(satRing12))

with open('satWeb.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(satWeb)
f.close()
with open('unsatWeb.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(unsatWeb)
f.close()
