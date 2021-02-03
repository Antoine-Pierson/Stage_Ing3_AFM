import numpy as np
import matplotlib.pyplot as plt
from pip._vendor.distlib.compat import raw_input
from my_package import utils as ui, myFonctions as mf
from pynput.keyboard import Listener
import keyboard


def moduleFrPts():
    typeOS = raw_input("Etes vous sous windows (w) ou mac (m)? (écrivez en minuscule)\n")
    path = raw_input("Entrez le chemin du dossier où se trouve les données à traiter\n")
    isPlot = False

    print("Voulez vous afficher les graphiques au fur et à mesure ? oui (o) non (n)")
    while True:
        try:
            if keyboard.is_pressed('o'):
                isPlot = True
                print("\nLes graphiques seront affichés")
                break
            elif keyboard.is_pressed('n'):
                print("\nLes graphiques ne seront pas affichés")
                isPlot = False
                break
        except: break

    fichiers, baseName = ui.listdirectory(path, typeOS, extension="txt")

    FrX = []
    FrY = []
    increment = 0
    while increment < len(fichiers):
        ##### Lecture du fichier txt #####

        verticalAB, timeStamp, zHeight, force = mf.returnDataFromFile(fichiers, increment)
        ptsArray = np.array([zHeight, force])

        if isPlot == True:
            plt.figure(figsize=(7.2, 4.8))
            plt.subplot(1, 2, 1)
            plt.plot(ptsArray[0], ptsArray[1], "blue")
            plt.ylabel("F (nN)")
            plt.xlabel("Z Height (nm) (piezo)")
            plt.title("Initial Force Curve")
            plt.grid()

        ##### correction piezo #####

        correctedPtsArray = mf.returnCorrectedCurve(ptsArray)

        if isPlot == True:
            plt.subplot(1, 2, 2)
            plt.plot(correctedPtsArray[0], correctedPtsArray[1], "blue")
            plt.ylabel("F (nN)")
            plt.xlabel("Z Height (nm)")
            plt.title("Force Curve corrected piezo")
            plt.grid()
            plt.show()

        ##### calcul variance et seuil pour trouver points de rupture #####

        posFrForceCurve = mf.returnPtsRupture(correctedPtsArray, isPlot)

        FrX.extend(posFrForceCurve[0])
        FrY.extend(posFrForceCurve[1])
        if isPlot == True:
            plt.figure(figsize=(7.2, 4.8))
            plt.plot(correctedPtsArray[0], correctedPtsArray[1], color="blue", label="Force Curve")
            plt.scatter(posFrForceCurve[0], posFrForceCurve[1], color="red", label="pics")
            plt.ylabel("F (nN)")
            plt.xlabel("Def")
            plt.title("Force Curve")
            plt.legend()
            plt.grid()
            plt.show()

        if isPlot == True:
            with Listener(on_press=ui.isBreak) as listener:
                print("Press the enter key to end the break")
                listener.join()

        increment += 1

    ##### module écriture données au format csv #####
    dictData = ['NameFiles', 'Z_Height', 'Force']
    outputCsvPath = mf.writeDataInCsvFile(path, baseName, FrX, FrY, dictData)
    print("Vos données sont enregistrées à l'adresse: " + outputCsvPath)


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
        plt.figure(figsize=(7.2, 4.8))
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
    print("Vos donnees sont enregistrees à l'adresse: " + outputCsvPath)

    ##### Affichage des stats - demande user #####
    print("Voulez vous afficher affichez les stats ? oui (o) non (n)")
    while True:
        try:
            if keyboard.is_pressed('o'):
                moduleStat(outputCsvPath)
                print("\nLes stats seront affichés")
                break
            elif keyboard.is_pressed('n'):
                print("\nLes stats ne seront pas affichés")
                break
        except:
            break


def moduleStat(outputPath):

    datas = mf.readDataInCsvFile(outputPath)

    plt.plot(datas["FMax"], datas.index)
    plt.show()

    return
