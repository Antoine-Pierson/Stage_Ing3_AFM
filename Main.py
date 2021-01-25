import numpy as np
import matplotlib.pyplot as plt
from pip._vendor.distlib.compat import raw_input
import MyFonctions as mf
import Utils as ui


def moduleFrPts():
    typeOS = raw_input("Etes vous sous windows ou mac ? (écrivez en minuscule)\n")
    path = raw_input("Entrez le path du dossier\n")
    fichiers, nameOutput = ui.listdirectory(path, typeOS)

    increment = 0
    while increment <= len(fichiers):
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
        dictData = ['Def', 'Force']
        mf.writeDataInCsvFile(path, posFrForceCurve[0], posFrForceCurve[1], dictData, nameOutput, increment)

        increment += 1


def moduleFmaxAire():
    typeOS = raw_input("Etes vous sous windows ou mac ? (écrivez en minuscule)\n")
    path = raw_input("Entrez le path du dossier\n")
    fichiers, nameOutput = ui.listdirectory(path, typeOS)

    increment = 0
    while increment <= len(fichiers):
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

        ##### Fmax ? #####

        curveRetour = ui.returnCurveSepareted(correctedPtsArray)[1]
        Fmax = max(curveRetour[1])

        ##### Aire sous la courbe #####

        aire = ui.AireSousCourbe(curveRetour)

        ##### module écriture données au format csv #####
        data1 = [Fmax]
        data2 = [aire]
        dictData = ['Fmax', 'Aire']
        mf.writeDataInCsvFile(path, data1, data2, dictData, nameOutput, increment)

        increment += 1


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
