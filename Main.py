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
        print("Application de la méthode du coin nord-ouest...")
        matrice_des_prop = lire_matrice_depuis_fichier(chemin_fichier)
        matrice_initiale = coin_nord_ouest(matrice_des_prop[1:])
        print("Résultat de la matrice du coin nord-ouest :")
        afficher_matrice_transfert(matrice_initiale)
        cout_total_nord_ouest = calculer_cout_total(matrice_des_couts[1:], matrice_initiale)
        print("Coût total pour la méthode du coin nord-ouest :", cout_total_nord_ouest)

        print("\n-------------------")
        print("Application de la méthode de Balas-Hammer...")
        matrice_transfert= balas_hammer(matrice_des_couts[1:], matrice_des_prop[1:])
        print("Résultat de la matrice de Balas-Hammer/Transfert :")
        afficher_matrice_transfert(matrice_transfert)
        if matrice_transfert is not None:
            cout_total_balas_hamer = calculer_cout_total(matrice_des_couts[1:], matrice_transfert)
            print("Coût total pour la méthode de Balas-Hamer :", cout_total_balas_hamer)

        print("\n-------------------")
        print("Vérification de la présence de cycles dans la matrice de transfert :")
        if detecter_cycle(matrice_transfert):
            maximiser_transport(matrice_transfert, matrice_des_couts)

        print("\n-------------------")
        print("La matrice de transfert est-elle connexe ? :")
        liste = verifier_connexite(matrice_transfert)

        print("\n-------------------")
        print("Rendre la matrice de transfert connexe si elle ne l'est pas :")
        composantes = verifier_connexite(matrice_transfert)
        rendre_connexe(composantes, matrice_transfert, matrice_des_couts)
        print("La matrice de transfert après avoir rendu connexe :")
        afficher_matrice_transfert(matrice_transfert)

        print("\n-------------------")
        print("Fin du programme.")


if __name__ == "__main__":
    main()
