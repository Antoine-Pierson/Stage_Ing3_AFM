import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import glob
import os.path
from pip._vendor.distlib.compat import raw_input
import Utils as ui

##### Lecture du fichier txt #####
def returnDataFromFile (fichiers, increment):

    f = open(fichiers[increment], 'r')
    verticalAB = []
    force = []
    zHeight = []
    timeStamp = []
    for i, line in enumerate(f):
        if i > 2:
            tmp = line.split()
            verticalAB.append(float(tmp[1]))
            force.append(float(tmp[2]))
            zHeight.append(float(tmp[3]) * math.pow(10, -9))
            timeStamp.append(float(tmp[4]))
    f.close()

    verticalAB = np.array(verticalAB)
    timeStamp = np.array(timeStamp)
    zHeight = np.array(zHeight)
    force = np.array(force)

    return verticalAB, timeStamp, zHeight, force


##### correction ligne de base, piezo #####
def returnCorrectedCurve (ptsArray):

    ##### fit points avec ligne de base
    a, b = np.polyfit(ptsArray[0][:500], ptsArray[1][:500], 1)

    newY = []
    for i in range(ptsArray.shape[1]):
        newY.append(ptsArray[1][i] - (a * ptsArray[0][i] + b))
    newPtsArray = np.array([ptsArray[0], np.array(newY)])

    ##### recherche du z0
    tmpCurveAller = np.array(ui.returnCurveSepareted(newPtsArray)[0])
    z0 = 0
    Fz0 = 0
    for i in range(1, tmpCurveAller.shape[1] - 1):
        if tmpCurveAller[1][i + 1] > 0 > tmpCurveAller[1][i - 1]:
            z0 = tmpCurveAller[0][i]
            Fz0 = tmpCurveAller[1][i]

    ##### correction décallage z0
    newX = []
    for i in range(newPtsArray.shape[1]):
        newX.append(newPtsArray[0][i] - z0)
    correctedPtsArray = np.array([np.array(newX), newPtsArray[1]])

    return correctedPtsArray


##### calcul variance et seuil pour trouver points de rupture #####
def returnPtsRupture (correctedPtsArray):

    curveRetour = ui.returnCurveSepareted(correctedPtsArray)[1]
    N = 10
    ##### Variance

    varI = ui.Var(list(curveRetour[1]), 0, N)

    ##### Seuil
    # alpha = 50
    alpha = float(input("Choose the alpha treshold\n"))
    seuil = ui.Seuil(curveRetour, alpha, N)
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

    """
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

    ##### Cherche Force d'adhésion avec position #####

    posFrForceCurveX = []
    posFrForceCurveY = []
    for i in range(curveRetour.shape[1]):
        for j in range(Fr.shape[1]):
            if i == Fr[0][j]:
                posFrForceCurveX.append(curveRetour[0][i])
                posFrForceCurveY.append(curveRetour[1][i])
    posFrForceCurve = np.array([posFrForceCurveX, posFrForceCurveY])

    return posFrForceCurve


##### module écriture données au format csv #####
def writeDataInCsvFile (outputPath, data1, data2, dictData, nameOutput, increment):
    zippedList = zip(data1, data2)
    dataFrame = pd.DataFrame(zippedList, columns=[dictData[0:]])
    dataFrame.to_csv(os.path.join(outputPath, nameOutput[increment] + '.csv'), sep=';')
