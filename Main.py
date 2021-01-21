from PIL import Image
import numpy as np
from PIL.TiffTags import TAGS
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import math
import csv
import pandas as pd
import glob
import os.path
from pip._vendor.distlib.compat import raw_input

##### Fonctions utiles #####

def listdirectory(path, typeOS):
    nameFichier = os.listdir(path)
    baseName = []
    for i in range(len(nameFichier)):
        baseName.append(os.path.basename(nameFichier[i]))
    baseName2 = []
    for line in baseName:
        tmp = line.split(".")
        baseName2.append(tmp[0])

    txt = ''
    if typeOS == "windows":
        path = path.replace('\'', '\\')
        txt = '\\*.txt'
    elif typeOS == "mac":
        path = path.replace('/', '//')
        txt = '//*.txt'
    else: print("Veulliez réessayer")

    fichier=[]
    l = glob.glob(path+txt)
    for i in l:
        if os.path.isdir(i): fichier.extend(listdirectory(i))
        else: fichier.append(i)

    return fichier, baseName2


def returnCurveSepareted (ptsArray):

    maxY = max(ptsArray[1])
    numPtsMax = 0
    for i in range(ptsArray.shape[1]):
        if ptsArray[1][i] == maxY:
            numPtsMax = i

    curveRetourX = []
    curveRetourY = []
    for i in range(numPtsMax, ptsArray.shape[1], 1):
        curveRetourX.append(ptsArray[0][i])
        curveRetourY.append(ptsArray[1][i])
    curveRetour = np.array([curveRetourX, curveRetourY])

    curveAllerX = []
    curveAllerY = []
    for i in range(0, numPtsMax, 1):
        curveAllerX.append(ptsArray[0][i])
        curveAllerY.append(ptsArray[1][i])
    curveAller = np.array([curveAllerX, curveAllerY])

    return curveAller, curveRetour


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

    return varI


def Seuil (curveRetour, alpha, N):
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

"""
def IsRupture(Fr, Fi):



   return rupturePts
"""

def Derivee (x, y):

    yp = (y[1:] - y[:-1]) / (x[1:] - x[:-1])

    plt.plot(x, y, label="f(x)")
    plt.plot(x[:-1], yp, label="f'(x)")

    plt.legend()
    plt.show()

    return yp

########################

typeOS = raw_input("Etes vous sous windows ou mac ? (écrivez en minuscule)\n")
path = raw_input("Entrez le path du dossier\n")
fichiers, nameOutput = listdirectory(path, typeOS)

increment = 0
#while increment <= len(fichiers):

    ##### Lecture du fichier txt #####

f = open(fichiers[0], 'r')
verticalAB = []
force = []
zHeight = []
timeStamp = []
for i,line in enumerate(f):
    if i > 2:
        tmp = line.split()
        verticalAB.append(float(tmp[1]))
        force.append(float(tmp[2]))
        zHeight.append(float(tmp[3])*math.pow(10, -9))
        timeStamp.append(float(tmp[4]))
f.close()

verticalAB = np.array(verticalAB)
timeStamp = np.array(timeStamp)

zHeight = np.array(zHeight)
force = np.array(force)
ptsArray = np.array([zHeight, force])

plt.figure(figsize=(19.2, 10.8))
plt.subplot(1, 2, 1)
plt.plot(ptsArray[0], ptsArray[1], "blue")
plt.ylabel("F (nN)")
plt.xlabel("Z Height (nm) (piezo)")
plt.title("Initial Force Curve")
plt.grid()

##### correction piezo #####

##### fit points avec ligne de base
'''
Adj = ptsArray[0][200] - ptsArray[0][150]
Opp = ptsArray[1][200] - ptsArray[1][150]
m = Opp/Adj
'''
a, b = np.polyfit(ptsArray[0][:500], ptsArray[1][:500], 1)

newY = []
for i in range(ptsArray.shape[1]):
    newY.append(ptsArray[1][i] - (a*ptsArray[0][i] + b))
newPtsArray = np.array([ptsArray[0], np.array(newY)])

##### recherche du z0
tmpCurveAller = np.array(returnCurveSepareted(newPtsArray)[0])
z0 = 0
Fz0 = 0
for i in range(1, tmpCurveAller.shape[1] - 1):
    if tmpCurveAller[1][i+1] > 0 > tmpCurveAller[1][i - 1]:
        z0 = tmpCurveAller[0][i]
        Fz0 = tmpCurveAller[1][i]
print(z0, Fz0)
##### correction décallage z0
newX = []
for i in range(newPtsArray.shape[1]):
    newX.append(newPtsArray[0][i] - z0)
correctedPtsArray = np.array([np.array(newX), newPtsArray[1]])

plt.subplot(1, 2, 2)
plt.plot(correctedPtsArray[0], correctedPtsArray[1], "blue")
plt.ylabel("F (nN)")
plt.xlabel("Z Height (nm)")
plt.title("Force Curve corrected piezo")
plt.grid()
plt.show()

##### calcul variance et seuil pour trouver points de rupture #####

curveRetour = returnCurveSepareted(correctedPtsArray)[1]
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
# yp = Derivee(curveRetour[0], curveRetour[1])

##### Seuil
alpha = 5e-3
#alpha = float(input("Choose the alpha treshold\n"))
seuil = Seuil(curveRetour, alpha, N)
tabSeuil = []
for i in range(varI.shape[1]):
    tabSeuil.append(seuil)

##### Pics de Rupture et conditions

Fi = curveRetour[1][1]
FrX = []
FrY = []
for i in range(1, varI.shape[1] - 1, 1):
    if varI[1][i] > seuil and varI[1][i - 1] < varI[1][i] and varI[1][i + 1] < varI[1][i]:
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

"""
rupturePts = IsRupture(Fr, Fi)
"""

##### Cherche Force d'adhésion avec position #####

posFrForceCurveX = []
posFrForceCurveY = []
for i in range(curveRetour.shape[1]):
    for j in range(Fr.shape[1]):
        if i == Fr[0][j]:
            posFrForceCurveX.append(curveRetour[0][i])
            posFrForceCurveY.append(curveRetour[1][i])
posFrForceCurve = np.array([posFrForceCurveX, posFrForceCurveY])

plt.figure(figsize=(19.2, 10.8))
plt.plot(correctedPtsArray[0], correctedPtsArray[1], color="blue", label="Force Curve")
plt.scatter(posFrForceCurve[0], posFrForceCurve[1], color="red", label="pics")
plt.ylabel("F (nN)")
plt.xlabel("Def")
plt.title("Force Curve")
plt.legend()
plt.grid()
plt.show()

##### module écriture données au format csv #####

zippedList = list(zip(posFrForceCurveX, posFrForceCurveY))
# print(zippedList)
dataFrame = pd.DataFrame(zippedList, columns=['Def', 'Force '])
dataFrame.to_csv(os.path.join(path, nameOutput[increment] + '.csv'), sep=';')

# df = pd.read_csv('test.csv', delimiter=';')
# print(df)

increment += 1

