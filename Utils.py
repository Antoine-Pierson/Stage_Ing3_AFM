import numpy as np
import matplotlib.pyplot as plt
import math
import glob
import os.path
from scipy import integrate as intg
from pylab import *

##### Fonctions utiles #####

def listdirectory(path, typeOS):

    txt = ''
    isEnd = False
    while not isEnd:
        if typeOS == "windows":
            path = path.replace('\'', '\\')
            txt = '\\*.txt'
            isEnd = True
        elif typeOS == "mac":
            path = path.replace('/', '//')
            txt = '//*.txt'
            isEnd = True
        else:
            print("Veulliez réessayer\n")
            isEnd = False

    fichier=[]
    l = glob.glob(path+txt)
    for i in l:
        if os.path.isdir(i): fichier.extend(listdirectory(i))
        else: fichier.append(i)

    baseName = []
    for i in range(len(l)):
        baseName.append(os.path.basename(l[i]))
    baseName2 = []
    for line in baseName:
        tmp = line.split(".")
        baseName2.append(tmp[0])

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
        tmp += Var(list(curveRetour[0]), 0, N)[0][i]
        #tmp += Var(list(curveRetour[1]), 0, N)[1][i]
    aveVar = tmp/50
    diffVar = 0
    for j in range(L-N-50, L-N, 1):
        diffVar += math.pow(Var(curveRetour[0], 0, N)[0][j] - aveVar, 2)
        #diffVar += math.pow(Var(curveRetour[1], 0, N)[1][j] - aveVar, 2)
    seuil = aveVar + alpha*math.sqrt(diffVar/50)

    return seuil


def AireSousCourbe(ptsArr):

    ia = 0
    ib = 0
    for i in range(1, ptsArr.shape[1] - 1):
        if ptsArr[1][i + 1] < 0 < ptsArr[1][i - 1]:
            ia = i
            break
    for i in range(1, ptsArr.shape[1] - 1):
        if ptsArr[1][i + 1] > 0 > ptsArr[1][i - 1]:
            ib = i
            break
    aire = 0
    for i in range(ia, ib - 5, 5):
        x = ptsArr[0][i + 5] - ptsArr[0][i]
        aire += ptsArr[1][i] * x

    return abs(aire)

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