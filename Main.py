import os
from fonctions import *

def main():
    chemin_dossier = os.path.join(os.path.dirname(__file__), 'Fichiers_tests')
    while True:
        nom_fichier = choisir_fichier(chemin_dossier)

        chemin_fichier = os.path.join(chemin_dossier, nom_fichier + ".txt")
        with open(chemin_fichier, 'r') as f:
            contenu = f.read()
            print("\nContenu du fichier {} :".format(nom_fichier))
            print(contenu)

        print("\n-------------------")
        print("Calcul de la matrice des coûts :")
        matrice_des_couts = lire_matrice_depuis_fichier(chemin_fichier)
        afficher_matrice_cout(matrice_des_couts[1:])

        print("\n-------------------")
        print("Calcul de la matrice de proposition de transport (Pi et Cj) :")
        matrice_des_prop = lire_matrice_depuis_fichier(chemin_fichier)
        afficher_matrice_proptrans(matrice_des_prop[1:])

        print("\n-------------------")
        print("Application de la méthode du coin nord-ouest :")
        matrice_des_prop = lire_matrice_depuis_fichier(chemin_fichier)
        matrice_initiale = coin_nord_ouest(matrice_des_prop[1:])
        afficher_matrice_nordouest(matrice_initiale)

        print("\n-------------------")
        print("Application de la méthode de Balas-Hammer :")
        capacites = matrice_des_prop[-1]
        balas_hammer(matrice_des_couts[1:], matrice_des_prop[1:], capacites)

        print("\n-------------------")
        print("Fin du programme.")

if __name__ == "__main__":
    main()
