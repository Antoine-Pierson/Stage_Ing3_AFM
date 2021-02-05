from my_package import modules as mod
from pip._vendor.distlib.compat import raw_input

##### Début du programme #####
def main():
    print("--------------------------\n"
          "-----START OF PROGRAM-----\n"
          "--------------------------\n")
    while True:
        try:
            _input = raw_input("Tapez 1 pour trouvez les points de ruptures utilisant la methode de la variance\n"
                               "Tapez 2 pour trouver F max et l aire sous la courbe\n")
            if _input == '1':
                print("Vous avez choisi le module de recherche des points de rupture par variance\n")
                mod.moduleFrPts()
                break
            elif _input == '2':
                print("Vous avez choisi le module de recherche de l'aire et de Fmax\n")
                mod.moduleFmaxAire()
                break
        except ValueError as err:
            print(err)
            break

    print("--------------------------\n"
          "------END OF PROGRAM------\n"
          "--------------------------\n")
    while True:
        try:
            end = raw_input("Appuyez sur 1 pour finir le program ! ")
            if end == '1':
                return False
        except ValueError as err:
            print(err)
