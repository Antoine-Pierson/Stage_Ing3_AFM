from PIL import Image
import numpy as np
from PIL.TiffTags import TAGS
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import math

##### Fonctions utiles #####

def Var (list, debut, N):
    var = []
    p = []
    for k in range(debut, len(list) - N, 1):
        tmp = []
        for l in range(k, k + N, 1):
            tmp.append(list[l])
        var.append(np.var(tmp, dtype=np.float64))
        p.append(k)
    varI = np.array([np.array(p), np.array(var)])

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


def Seuil (curveRetour, alpha, N, debut):
    L = curveRetour.shape[1]
    tmp = 0
    for i in range(L-N-50, L-N, 1):
        #tmp += Var(list(curveRetour[0]), 0, N)[0][i]
        tmp += Var(list(curveRetour[1]), 0, N)[1][i]
    aveVar = tmp/50
    diffVar = 0
    for j in range(L-N-50, L-N, 1):
        #diffVar += math.pow(Var(curveRetour[0], 0, N)[0][j] - aveVar, 2)
        diffVar += math.pow(Var(curveRetour[1], 0, N)[1][j] - aveVar, 2)
    seuil = aveVar + alpha*math.sqrt(diffVar/50)

    return seuil


def IsRupture(Fr, Fi):



    return rupturePts


def Derivee (x, y):

    yp = (y[1:] - y[:-1]) / (x[1:] - x[:-1])

    plt.plot(x, y, label="f(x)")
    plt.plot(x[:-1], yp, label="f'(x)")

    plt.legend()
    plt.show()

    return yp
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
plt.subplot(1, 2, 1)
plt.plot(ptsArray[0], ptsArray[1], "blue")
plt.ylabel("F (nN)")
plt.xlabel("Z (piezo)")
plt.title("Initial Force Curve")
plt.grid()

##### correction piezo #####

tmp = 0
a = 0
r = 400
for i in range(r):
    tmp += ptsArray[1][i]
a = tmp / r
for i in range(ptsArray.shape[1]):
    ptsArray[1][i] -= a

plt.subplot(1, 2, 2)
plt.plot(ptsArray[0], ptsArray[1], "blue")
plt.ylabel("F (nN)")
plt.xlabel("d (nm)")
plt.title("Force Curve corrected piezo")
plt.grid()
plt.show()

##### calcul variance et seuil pour trouver points de rupture #####

maxY = max(ptsArray[1])
debut = 0
for i in range(ptsArray.shape[1]):
    if ptsArray[1][i] == maxY:
        debut = i

curveRetourX = []
curveRetourY = []
for i in range(debut, ptsArray.shape[1], 1):
    curveRetourX.append(ptsArray[0][i])
    curveRetourY.append(ptsArray[1][i])
curveRetour = np.array([curveRetourX, curveRetourY])

N = 10
##### Variance

varI = Var(list(curveRetour[1]), 0, N)

plt.figure(figsize=(19.2, 10.8))
plt.ylabel("Var(i)")
plt.xlabel("i")
plt.title("----")
plt.grid()
plt.plot(varI[0], varI[1], "blue")
plt.show()
#yp = Derivee(curveRetour[0], curveRetour[1])

##### Seuil

#listPtsX = list(ptsArray[0])
alpha = float(input("Choose the alpha treshold\n"))
seuil = Seuil(curveRetour, alpha, N, debut)
tabSeuil = []
for i in range(varI.shape[1]):
    tabSeuil.append(seuil)
print(seuil)
plt.figure(figsize=(19.2, 10.8))
plt.plot(varI[0], varI[1], color="blue", label="Var(i)")
plt.plot(list(varI[0]), tabSeuil, color="orange", label="seuil")
plt.ylabel("Var(i)")
plt.xlabel("i")
plt.title("----")
plt.legend()
plt.grid()
plt.show()

##### Pics de Rupture et conditions

Fi = np.array(curveRetourY[1])
FrX = []
FrY = []
for i in range(1, varI.shape[1]-1, 1):
    if varI[1][i] > seuil and varI[1][i-1] < varI[1][i] and varI[1][i+1] < varI[1][i]:
        FrY.append(varI[1][i])
        FrX.append(varI[0][i])
Fr = np.array([FrX, FrY])
plt.figure(figsize=(19.2, 10.8))
plt.plot(varI[0], varI[1], color="blue", label="Var(i)")
plt.plot(list(varI[0]), tabSeuil, color="orange", label="seuil")
plt.scatter(Fr[0], Fr[1], color="red", label="pics")
plt.ylabel("Var(i)")
plt.xlabel("i")
plt.title("----")
plt.legend()
plt.grid()
plt.show()

rupturePts = IsRupture(Fr, Fi)


##### calcul Force d'adhésion avec position #####