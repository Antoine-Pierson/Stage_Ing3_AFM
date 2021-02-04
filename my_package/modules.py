import numpy as np
import matplotlib.pyplot as plt
from pip._vendor.distlib.compat import raw_input
from my_package import myFonctions as mf
from my_package import utils as ui


def moduleFrPts():
    typeOS = ""
    while True:
        try:
            typeOS = raw_input("Etes vous sous windows (w) ou mac (m)? (écrivez en minuscule)\n")
            if typeOS == 'w' or typeOS == 'm' or typeOS == 'windows' or typeOS == 'mac':
                break
        except ValueError as err:
            print(err)
            break

    path = ""
    while True:
        try:
            path = raw_input("Entrez le chemin du dossier où se trouve les données à traiter\n")
            if ui.isPathExist(path):
                break
        except:
            print("Incorrect Path")
            break

    isPlot = False
    cstAlpha = 0
    while True:
        try:
            u_input = raw_input("Voulez vous afficher les graphiques au fur et à mesure ? oui (o) non (n)\n")
            if u_input == 'o' or u_input == 'oui':
                isPlot = True
                print("Les graphiques seront affichés")
                break
            elif u_input == 'n' or u_input == 'non':
                isPlot = False
                print("Les graphiques ne seront pas affichés")
                cstAlpha = int(input("Veuillez donc pas conséquent choisir une valeur de alpha pour le seuil: "))
                break
        except ValueError as err:
            print(err)
            break

    fichiers, baseName = ui.listdirectory(path, typeOS, extension="txt")

    FrX = []
    FrY = []
    increment = 0
    while increment < len(fichiers):
        print("Traitement en cours ! Fichier ", increment+1, "/", len(fichiers))

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

        posFrForceCurve = mf.returnPtsRupture(correctedPtsArray, isPlot, cstAlpha)

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

        increment += 1

    ##### module écriture données au format csv #####
    dictData = ['NameFiles', 'Z_Height', 'Force']
    outputCsvPath = mf.writeDataInCsvFile(path, baseName, FrX, FrY, dictData)
    print("Vos données sont enregistrées à l'adresse: " + outputCsvPath)


def moduleFmaxAire():
    typeOS = ""
    while True:
        try:
            typeOS = raw_input("Etes vous sous windows (w) ou mac (m)? (écrivez en minuscule)\n")
            if typeOS == 'w' or typeOS == 'm' or typeOS == 'windows' or typeOS == 'mac':
                break
        except ValueError as err:
            print(err)
            break

    path = ""
    while True:
        try:
            path = raw_input("Entrez le chemin du dossier où se trouve les données à traiter\n")
            if ui.isPathExist(path):
                break
        except:
            print("Incorrect Path")
            break

    isPlot = False

    while True:
        try:
            input = raw_input("Voulez vous afficher les graphiques au fur et à mesure ? oui (o) non (n)\n")
            if input == 'o' or input == 'oui':
                isPlot = True
                print("Les graphiques seront affichés")
                break
            elif input == 'n' or input == 'non':
                isPlot = False
                print("Les graphiques ne seront pas affichés")
                break
        except ValueError as err:
            print(err)
            break

    fichiers, baseName = ui.listdirectory(path, typeOS, extension="txt")

    FMax = []
    aire = []
    increment = 0
    indexDelete = 0
    while increment < len(fichiers):
        print("Traitement en cours ! Fichier ", increment + 1, "/", len(fichiers))

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

        ##### Fmax ? #####

        curveRetour = ui.returnCurveSepareted(correctedPtsArray)[1]

        ##### Aire sous la courbe  + FMax #####
        _aire = ui.aireSousCourbe(curveRetour)[0]
        if _aire != 0:
            A, ymean = ui.aireSousCourbe(curveRetour)
            aire.append(A)
            FMax.append(abs(min(curveRetour[1])) - abs(ymean))
        else:
            del baseName[increment - indexDelete]
            indexDelete += 1

        increment += 1

        #### J'aurai bien aimé faire ça en utilisant la dérivée mais ça marche pas...
        #### Du moins la dérivée que je fait localement ne me retourne pas vraiment ce que je veux
        '''
        isOk = False
        yp = ui.derivee(curveRetour[0], curveRetour[1])
        
        for i in range(len(yp)):
            if int(yp[i]) == 0:
                isOk = True
                
        if isOk == True:
            FMax = min(curveRetour[1])
            imax = 0
            for i in range(curveRetour.shape[1]):
                if FMax == curveRetour[1][i]:
                    imax = i
            m1 = (curveRetour[1][imax] - curveRetour[1][imax-10])/(curveRetour[0][imax] - curveRetour[0][imax-10])
            m2 = (curveRetour[1][imax] - curveRetour[1][imax + 10]) / (curveRetour[0][imax] - curveRetour[0][imax + 10])
            
            if m1 < 0 and m2 > 0: # ça veut dire qu'il existe un vrai max
                ##### Aire sous la courbe  + FMax #####
                A, ymean = ui.aireSousCourbe(curveRetour)
                aire.append(A)
                FMax.append(abs(min(curveRetour[1])) - abs(ymean))
        else:
            del baseName[increment - indexDelete]
            indexDelete += 1
        increment += 1
        '''


    ##### module écriture données au format csv #####
    dictData = ["NameFiles", "FMax", "Aire"]
    outputCsvPath = mf.writeDataInCsvFile(path, baseName, FMax, aire, dictData)
    print("Vos donnees sont enregistrees à l'adresse: " + outputCsvPath)

    ##### Affichage des stats - demande user #####
    while True:
        try:
            input = raw_input("Voulez vous afficher les stats ? oui (o) non (n)\n")
            if input == 'o' or input == 'oui':
                print("Les stats seront affichés")
                moduleStat(outputCsvPath)
                break
            elif input == 'n' or input == 'non':
                print("Les stats ne seront pas affichés")
                break
        except ValueError as err:
            print(err)
            break


def moduleStat(outputPath):

    datas = mf.readDataInCsvFile(outputPath)
    print("A venir prochainement !")
    #plt.plot(datas["FMax"], datas.index)
    #plt.show()

    return
