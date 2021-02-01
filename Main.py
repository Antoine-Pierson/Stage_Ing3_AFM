import numpy as np
import matplotlib.pyplot as plt
import scipy
from pip._vendor.distlib.compat import raw_input
import MyFonctions as mf
import Utils as ui


def moduleFrPts():
    typeOS = raw_input("Etes vous sous windows (w) ou mac (m)? (écrivez en minuscule)\n")
    path = raw_input("Entrez le chemin du dossier où se trouve les données à traiter\n")
    fichiers, baseName = ui.listdirectory(path, typeOS, extension="txt")

    FrX = []
    FrY = []
    increment = 0
    while increment < len(fichiers):
        ##### Lecture du fichier txt #####

        verticalAB, timeStamp, zHeight, force = mf.returnDataFromFile(fichiers, increment)
        ptsArray = np.array([zHeight, force])

        plt.figure(figsize=(19.2, 10.8))
        plt.subplot(1, 2, 1)
        plt.plot(ptsArray[0], ptsArray[1], "blue")
        plt.ylabel("F (nN)")
        plt.xlabel("Z Height (nm) (piezo)")
        plt.title("Initial Force Curve")
        plt.grid()

        ##### correction piezo #####

        correctedPtsArray = mf.returnCorrectedCurve(ptsArray)

        plt.subplot(1, 2, 2)
        plt.plot(correctedPtsArray[0], correctedPtsArray[1], "blue")
        plt.ylabel("F (nN)")
        plt.xlabel("Z Height (nm)")
        plt.title("Force Curve corrected piezo")
        plt.grid()
        plt.show()

        ##### calcul variance et seuil pour trouver points de rupture #####

        posFrForceCurve = mf.returnPtsRupture(correctedPtsArray)

        FrX.extend(posFrForceCurve[0])
        FrY.extend(posFrForceCurve[1])

        plt.figure(figsize=(19.2, 10.8))
        plt.plot(correctedPtsArray[0], correctedPtsArray[1], color="blue", label="Force Curve")
        plt.scatter(posFrForceCurve[0], posFrForceCurve[1], color="red", label="pics")
        plt.ylabel("F (nN)")
        plt.xlabel("Def")
        plt.title("Force Curve")
        plt.legend()
        plt.grid()
        plt.show()

        isOk = False
        while not isOk:
            choix = int(raw_input("press 1: "))
            if choix == 1:
                isOk = True
            else: isOk = False

        increment += 1

    ##### module écriture données au format csv #####
    dictData = ['NameFiles', 'Z_Height', 'Force']
    outputCsvPath = mf.writeDataInCsvFile(path, baseName, FrX, FrY, dictData)
    print("Vos données sont enregistrées à l'adresse: " + outputCsvPath)
    '''
    isEnd3 = False
    while not isEnd3:
        print("Tapez 1 si vous voulez vous affichez les stats\nTapez 0 si non\n")
        isContinue = int(raw_input("Votre choix: "))
        if isContinue == 1:
            moduleStat(outputCsvPath)
            isEnd3 = True
        elif isContinue == 0:
            isEnd3 = True
        else:
            print("Veuillez reessayer")
            isEnd3 = False
    '''


def moduleFmaxAire():
    typeOS = raw_input("Etes vous sous windows (w) ou mac (m)? (écrivez en minuscule)\n")
    path = raw_input("Entrez le chemin du dossier où se trouve les données à traiter\n")
    fichiers, baseName = ui.listdirectory(path, typeOS, extension="txt")

    FMax = []
    aire = []
    increment = 0
    indexDelete = 0
    while increment < len(fichiers):
        ##### Lecture du fichier txt #####

        verticalAB, timeStamp, zHeight, force = mf.returnDataFromFile(fichiers, increment)
        ptsArray = np.array([zHeight, force])
        '''
        plt.figure(figsize=(19.2, 10.8))
        plt.subplot(1, 2, 1)
        plt.plot(ptsArray[0], ptsArray[1], "blue")
        plt.ylabel("F (nN)")
        plt.xlabel("Z Height (nm) (piezo)")
        plt.title("Initial Force Curve")
        plt.grid()
        '''
        ##### correction piezo #####

        correctedPtsArray = mf.returnCorrectedCurve(ptsArray)
        '''
        plt.subplot(1, 2, 2)
        plt.plot(correctedPtsArray[0], correctedPtsArray[1], "blue")
        plt.ylabel("F (nN)")
        plt.xlabel("Z Height (nm)")
        plt.title("Force Curve corrected piezo")
        plt.grid()
        plt.show()
        '''
        ##### Fmax ? #####

        curveRetour = ui.returnCurveSepareted(correctedPtsArray)[1]

        #yp = ui.Derivee(curveRetour[0], curveRetour[1])
        #FMax.append(min(curveRetour[1]))
        '''
        yp_max = max(abs(yp))
        
        for i in range(len(yp)):
            if abs(yp[i]) == yp_max:
                FMax.append(curveRetour[1][i])
                break
        '''
        ##### Aire sous la courbe  + FMax #####
        _aire = ui.AireSousCourbe(curveRetour)[0]
        if _aire != 0:
            A, ymean = ui.AireSousCourbe(curveRetour)
            aire.append(A)
            FMax.append(abs(min(curveRetour[1])) - abs(ymean))
        else:
            del baseName[increment - indexDelete]
            indexDelete += 1

        increment += 1

    ##### module écriture données au format csv #####
    dictData = ["NameFiles", "FMax", "Aire"]
    outputCsvPath = mf.writeDataInCsvFile(path, baseName, FMax, aire, dictData)
    print("Vos données sont enregistrées à l'adresse: " + outputCsvPath)

    isEnd2 = False
    while not isEnd2:
        print("Tapez 1 si vous voulez affichez les stats\nTapez 0 si non\n")
        isContinue = int(raw_input("Votre choix: "))
        if isContinue == 1:
            moduleStat(outputCsvPath)
            isEnd2 = True
        elif isContinue == 0:
            isEnd2 = True
        else:
            print("Retry !")
            isEnd2 = False


def moduleStat(outputPath):

    datas = mf.readDataInCsvFile(outputPath)

    plt.plot(datas["FMax"], datas.index)
    plt.show()

    return


isEnd = False
while not isEnd:
    print("Tapez 1 pour trouvez les points de ruptures utilisant la methode de la variance\n"
          "Tapez 2 pour trouver F max et l aire sous la courbe\n")
    option = int(raw_input("Votre choix: "))

    if option == 1:
        moduleFrPts()
        isEnd = True
    elif option == 2:
        moduleFmaxAire()
        isEnd = True
    else:
        print("Retry !")
        isEnd = False
