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

            reponse = input("Voulez-vous afficher la matrice des coûts ? (oui/non) : ")
            if reponse.lower() == "oui":
                matrice_des_couts = lire_matrice_depuis_fichier(chemin_fichier)
                print("Matrice des coûts :")
                afficher_matrice_cout(matrice_des_couts[1:])

            reponse2 = input("Voulez-vous afficher la matrice de proposition de transport ? (oui/non) : ")
            if reponse2.lower() == "oui":
                matrice_des_prop = lire_matrice_depuis_fichier(chemin_fichier)
                print("Matrice de proposition de transport (Pi et Cj) :")
                afficher_matrice_proptrans(matrice_des_prop[1:])

            response3 = input("Voulez-vous résoudre le problème de transport avec la méthode du coin nord-ouest ? (oui/non) : ")
            if response3.lower() == "oui":
                matrice_des_prop = lire_matrice_depuis_fichier(chemin_fichier)
                matrice_initiale = coin_nord_ouest(matrice_des_prop[1:])
                afficher_matrice_transfert(matrice_initiale)

            capacites = matrice_des_prop[-1]
            reponse4 = input("Voulez-vous résoudre le problème de transport avec la méthode de Balas-Hammer ? (oui/non) : ")
            if reponse4.lower() == "oui":
                balas_hammer(matrice_des_couts[1:], matrice_des_prop[1:], capacites)

            print("Fin du programme.")

if __name__ == "__main__":
    main()
