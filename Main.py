from PIL import Image
import numpy as np
from PIL.TiffTags import TAGS
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import math

"""
im = Image.open('Si__010.tiff')
im.show()
print(np.size(im))

imarray = np.array(im)
print(np.shape(imarray))

with Image.open('Si__010.tiff') as img:
    meta_dict = {TAGS[key] : img.tag[key] for key in img.tag.iterkeys()}
"""
###########

"""
img = mpimg.imread('Si__010.tiff')
print(type(img)) # c'est un numpy array
plt.imshow(img) # show image
plt.show()
for i in img:
    print(i)
"""

########################

##### Fonctions utiles #####

def Var (listF, debut, N):
    var = []
    p = []
    _somme = 0
    print(type(listF))
    for k in range(debut, len(listF) - N, N):
        tmp = []
        for l in range(k, k + N, 1):
            tmp.append(listF[l])
        var.append(np.var(tmp))
        p.append(k)
    varI = np.array([np.array(var), np.array(p)])

    """
    while isRun:
        sFi = 0
        for k in range(debut, debut + N):
            sFi += listF[k]
        sFi *= 1 / N

        for i in range(debut, debut + N):
            _somme += math.sqrt(listF[i + N] - sFi)
        _somme *= 1/N
        var.extend(_somme)

        debut += N
        if debut > len(listF):
            isRun = False
    """
    return varI



########################

f = open('lot courbes de forces/1.txt', 'r')
# content = f.readlines()
x = []
y = []
# print(content[0][0])
for line in f:
    line = line.split()
    x.append(float(line[0]))
    y.append(float(line[1]))
f.close()
x = np.array(x)
y = np.array(y)
ptsArray = np.array([x, y])
# print(ptsArray[0][0], " ", ptsArray[1][0])

plt.figure(figsize=(19.2, 10.8))
plt.ylabel("F (nN)")
plt.xlabel("Z (piezo)")
plt.title("Force Curve")
plt.grid()
plt.plot(ptsArray[0], ptsArray[1], "blue")
plt.show()

##### correction piezo #####

tmp = 0
a = 0
r = 400
for i in range(r):
    tmp += ptsArray[1][i]
a = tmp / r
for i in range(ptsArray.shape[1]):
    ptsArray[1][i] -= a

plt.figure(figsize=(19.2, 10.8))
plt.ylabel("F (nN)")
plt.xlabel("d (nm)")
plt.title("Force Curve")
plt.grid()
plt.plot(ptsArray[0], ptsArray[1], "blue")
plt.show()

##### calcul variance et seuil pour trouver points de rupture #####

N = 10
listPtsY = list(ptsArray[1])
maxY = max(ptsArray[1])
debut = 0
for i in range(ptsArray.shape[1]):
    if ptsArray[1][i] == maxY:
        debut = i
varI = Var(listPtsY, debut, N)

plt.figure(figsize=(19.2, 10.8))
plt.ylabel("Var(i)")
plt.xlabel("i")
plt.title("Force Curve")
plt.grid()
plt.plot(varI[0], varI[1], "blue")
plt.show()




##### calcul Force d'adhésion avec position #####