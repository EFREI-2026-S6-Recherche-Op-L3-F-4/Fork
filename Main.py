import os
from itertools import zip_longest

def demander_chemin_dossier():
    chemin = input("Veuillez entrer le chemin du dossier contenant vos fichiers de matrice : ")
    while not os.path.exists(chemin):
        print("Chemin non trouvé")
        chemin = input("Veuillez entrer le chemin du dossier : ")
    return chemin

# Fonction pour lire une matrice à partir d'un fichier texte
def lire_matrice_depuis_fichier(chemin_fichier):
    matrice = []
    with open(chemin_fichier, 'r') as f:
        for ligne in f:
            # Supprimer les espaces blancs et diviser la ligne en valeurs individuelles
            valeurs_ligne = [int(valeur) for valeur in ligne.strip().split()]
            # Ajouter la ligne à la matrice
            matrice.append(valeurs_ligne)
    return matrice


def afficher_matrice_cout(matrice_des_couts):
    for ligne in matrice_des_couts[:-1]:
        print("[", end="")
        for element in ligne[:-1]:
            # Chaque élément est affiché avec une largeur de champ de 4, aligné à droite
            print(f"{element:4}", end="  ")
        print("]")


def afficher_matrice_proptrans(matrice_des_prop):
    # Afficher la dernière colonne (provisions)
    print("Provisions : [", end="")
    for ligne in matrice_des_prop[:-1]:
        # Les éléments de provision sont alignés
        print(f"{ligne[-1]:4}", end=" ")
    print("]")

    # Afficher la dernière ligne (commandes)
    print("Commandes : [", end="")
    for element in matrice_des_prop[-1]:
        # Les éléments de commande sont alignés
        print(f"{element:4}", end=" ")
    print("]")


# Fonction pour choisir un fichier dans un dossier
def choisir_fichier(dossier):
    fichiers = os.listdir(dossier)
    print("Liste des problèmes de transport dans le dossier :")
    for fichier in fichiers:
        print(fichier)
    nom_fichier = input("Entrez le nom du fichier que vous voulez afficher : ")
    return nom_fichier


def coin_nord_ouest(matrice_des_prop):
    # Utiliser des copies pour éviter de modifier la matrice originale
    provisions = [ligne[-1] for ligne in matrice_des_prop[:-1]].copy()  # Extraire les provisions de chaque ligne, sauf la dernière
    commandes = matrice_des_prop[-1].copy()  # Extraire les commandes en faisant une copie complète
    n = len(provisions)  # Nombre de sources (lignes)
    m = len(commandes)  # Nombre de destinations (colonnes)

    matrice_transfert = [[0 for _ in range(m)] for _ in range(n)]  # Initialiser la matrice de transfert à zéro

    i = j = 0  # Indices pour parcourir les sources et les destinations
    while i < n and j < m:
        transfert = min(provisions[i], commandes[j])  # Quantité à transférer basée sur le minimum
        matrice_transfert[i][j] = transfert
        provisions[i] -= transfert  # Réduire la provision après transfert
        commandes[j] -= transfert  # Réduire la commande après transfert
        if provisions[i] == 0: # Passer à la prochaine source
            i += 1
        if commandes[j] == 0: # Passer à la prochaine destination
            j += 1

    return matrice_transfert


# Pour un affichage + lisible de la fonction nord ouest
def afficher_matrice_transfert(matrice_transfert):
    print("Résultat de la méthode du coin nord-ouest :")
    for ligne in matrice_transfert:
        print("[", end="")
        for element in ligne:
            print(f"{element:4}", end=" ")
        print("]")


def balas_hammer(matrice_des_couts, matrice_des_prop, capacites):
    # Calcul des pénalités pour les lignes
    penalites_lignes = [sorted(ligne)[:2] for ligne in matrice_des_couts[:-1]]
    penalites_lignes = [penalites[1] - penalites[0] for penalites in penalites_lignes]
    print("Pénalités pour les lignes :", penalites_lignes)

    # Calcul des pénalités pour les colonnes
    penalites_colonnes = [sorted(colonne)[:2] for colonne in zip_longest(*matrice_des_couts, fillvalue=0)][:-1]
    penalites_colonnes = [penalites[1] - penalites[0] for penalites in penalites_colonnes]
    print("Pénalités pour les colonnes :", penalites_colonnes)

    # Trouver la pénalité maximale
    max_penalite_ligne = max(penalites_lignes)
    max_penalite_colonne = max(penalites_colonnes)

    # Déterminer le type de pénalité maximale et son indice
    if max_penalite_ligne > max_penalite_colonne:
        penalites_type = "ligne"
        indice = penalites_lignes.index(max_penalite_ligne)
        max_penalite = max_penalite_ligne
    elif max_penalite_ligne < max_penalite_colonne :
        penalites_type = "colonne"
        indice = penalites_colonnes.index(max_penalite_colonne)
        max_penalite = max_penalite_colonne

    # max_penalite_ligne == max_penalite_colonne
    else:
        print("Les pénalités maximales sont égales pour les lignes et les colonnes.")
        # Obtenir les indices des lignes avec la même pénalité maximale
        indices_lignes_max = [i for i, p in enumerate(penalites_lignes) if p == max_penalite_ligne]
        # Obtenir les indices des colonnes avec la même pénalité maximale
        indices_colonnes_max = [i for i, p in enumerate(penalites_colonnes) if p == max_penalite_colonne]
        print("Indices des lignes avec la même pénalité maximale :", indices_lignes_max)
        print("Indices des colonnes avec la même pénalité maximale :", indices_colonnes_max)
        if all(p == max_penalite_ligne for p in penalites_lignes):
            # Si toutes les pénalités égales sont dans les lignes, choix première ligne
            print("Si toutes les pénalités égales sont dans les lignes")
            penalites_type = "ligne"
            indice = penalites_lignes.index(max_penalite_ligne)
        elif all(p == max_penalite_colonne for p in penalites_colonnes):
            # Si toutes les pénalités égales sont dans les colonnes, choix première colonne
            print("Si toutes les pénalités égales sont dans les colonnes")
            penalites_type = "colonne"
            indice = penalites_colonnes.index(max_penalite_colonne)
        else:
            # Si les pénalités égales sont réparties entre lignes et colonnes, choisir en fonction de la plus grande pénalité
            print("Si les pénalités égales sont réparties entre lignes et colonnes, choisir arbitrairement : ici colonne")
            penalites_type = "ligne" if max_penalite_ligne > max_penalite_colonne else "colonne"
            indice = indices_lignes_max[0] if penalites_type == "ligne" else indices_colonnes_max[0]
        max_penalite = max_penalite_ligne if penalites_type == "ligne" else max_penalite_colonne

    # Déterminer l'arête à remplir
    # Déterminer l'arête à remplir
    if penalites_type == "ligne":
        arete = [indice, matrice_des_prop[-2].index(
            min(matrice_des_prop[-2]))]  # Trouver l'indice de la colonne avec le minimum dans la ligne
    else:
        arete = [matrice_des_prop.index(min(matrice_des_prop[:-1], key=lambda x: x[indice])),
                 indice]  # Trouver l'indice de la ligne avec le minimum dans la colonne
    # Afficher les informations
    print(f"Pénalité maximale de valeur {max_penalite} située en {penalites_type} {indice}.")

    if matrice_des_prop[arete[0]][arete[1]] == max_penalite:
        print("Il y a plusieurs endroits avec la même valeur de pénalité maximale.")

    # Déterminer la quantité maximale à déplacer
    quantite_max = min(capacites[arete[0]], capacites[arete[1]])
    print(f"Remplir l'arête {arete} avec une quantité maximale de {quantite_max}")

    # Mettre à jour les capacités
    capacites[arete[0]] -= quantite_max # Réduire la capacité de la ligne
    capacites[arete[1]] -= quantite_max # Réduire la capacité de la colonne


# Programme principal
def main():
    chemin_dossier = demander_chemin_dossier()
    while True :
        nom_fichier = choisir_fichier(chemin_dossier)

        if nom_fichier + ".txt" in os.listdir(chemin_dossier):
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

        else:
            print("Le fichier spécifié n'existe pas dans le dossier.")


if __name__ == "__main__":
    main()


