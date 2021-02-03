from my_package import modules as mod
from my_package import utils as ui
import keyboard
from pynput.keyboard import Listener

##### Début du programme #####
def run():
    print("Tapez 1 pour trouvez les points de ruptures utilisant la methode de la variance\n"
          "Tapez 2 pour trouver F max et l aire sous la courbe\n")
    while True:
        try:
            if keyboard.is_pressed('1'):
                print("\nVous avez choisi le module de recherche des points de rupture par variance\n")
                mod.moduleFrPts()
                break
            elif keyboard.is_pressed('2'):
                print("\nVous avez choisi le module de recherche de l'aire et de Fmax\n")
                mod.moduleFmaxAire()
                break
        except: break
    with Listener(on_press=ui.breakEnd) as listener:
        print("Press the enter key to end")
        listener.join()