import math
import glob
import os.path
from pylab import *

##### Fonctions utiles #####

def isPathExist(path: str) -> bool:
    if os.path.exists(path):
        return True
    else:
        print("Le chemin ", path, " n'existe pas")
        return False


def listdirectory(path, typeOS, extension):

    txt = ''
    isEnd = False
    while not isEnd:
        if typeOS == "windows" or "w":
            path = path.replace('\'', '\\')
            txt = '\\*.' + extension
            isEnd = True
        elif typeOS == "mac" or "m":
            path = path.replace('/', '//')
            txt = '//*.' + extension
            isEnd = True
        else:
            print("Veuillez réessayer\n")
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


def var (list, debut, N):
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


def seuil (curveRetour, alpha, N):
    L = curveRetour.shape[1]
    tmp = 0
    for i in range(L-N-50, L-N, 1):
        #tmp += Var(list(curveRetour[0]), 0, N)[0][i]
        tmp += var(list(curveRetour[1]), 0, N)[1][i]
    aveVar = tmp/50
    diffVar = 0
    for j in range(L-N-50, L-N, 1):
        #diffVar += math.pow(Var(curveRetour[0], 0, N)[0][j] - aveVar, 2)
        diffVar += math.pow(var(curveRetour[1], 0, N)[1][j] - aveVar, 2)
    seuil = aveVar + alpha*math.sqrt(diffVar/50)

    return seuil


##### Retourne la valeur absolue de L'aire sous la courbe de retour
##### et la valeur moyenne en y de la ligne de base de retour pour rectifier FMax
def aireSousCourbe(ptsArr):

    tmp = 0
    reversedArrY = ptsArr[1][::-1]
    for i in range(0, 100, 1):
        tmp += reversedArrY[i]
    ymean = tmp/100 #ymean est la moyenne en y de notre ligne de base de retour calculé sur 100 pts

    ia = 0
    ib = 0
    for i in range(1, ptsArr.shape[1] - 5):
        if ptsArr[1][i + 5] < ymean < ptsArr[1][i - 5]:
            ia = i
            break

    for i in range(ia, ptsArr.shape[1] - 5):
        if ptsArr[1][i + 5] > ymean > ptsArr[1][i - 5]:
            ib = i
            break

    aire = 0
    for i in range(ia, ib - 2, 2): # stop=ib - 2
        x = ptsArr[0][i + 2] - ptsArr[0][i]
        aire += ptsArr[1][i] * x

    return abs(aire), ymean


##### retourne une approximation de dérivées à chaque pts #####
def derivee (x, y):
    yp = np.diff(y)/np.diff(x)

    #yp = (y[1:] - y[:-1]) / (x[1:] - x[:-1])

    return yp


########################