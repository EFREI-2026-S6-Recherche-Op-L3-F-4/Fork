import os
from itertools import zip_longest

def demander_chemin_dossier():
    chemin = input("Veuillez entrer le chemin du dossier contenant vos fichiers de matrice : ")
    while not os.path.exists(chemin):
        print("Chemin non trouvé")
        chemin = input("Veuillez entrer le chemin du dossier : ")
    return chemin

def lire_matrice_depuis_fichier(chemin_fichier):
    matrice = []
    with open(chemin_fichier, 'r') as f:
        for ligne in f:
            valeurs_ligne = [int(valeur) for valeur in ligne.strip().split()]
            matrice.append(valeurs_ligne)
    return matrice

def afficher_matrice_cout(matrice_des_couts):
    for ligne in matrice_des_couts[:-1]:
        print("[", end="")
        for element in ligne[:-1]:
            print(f"{element:4}", end="  ")
        print("]")

def afficher_matrice_proptrans(matrice_des_prop):
    print("Provisions : [", end="")
    for ligne in matrice_des_prop[:-1]:
        print(f"{ligne[-1]:4}", end=" ")
    print("]")

    print("Commandes : [", end="")
    for element in matrice_des_prop[-1]:
        print(f"{element:4}", end=" ")
    print("]")

def choisir_fichier(dossier):
    fichiers = os.listdir(dossier)
    print("Liste des problèmes de transport dans le dossier :")
    for fichier in fichiers:
        print(fichier)
    nom_fichier = input("Entrez le nom du fichier que vous voulez afficher : ")
    return nom_fichier

def coin_nord_ouest(matrice_des_prop):
    provisions = [ligne[-1] for ligne in matrice_des_prop[:-1]].copy()
    commandes = matrice_des_prop[-1].copy()
    n = len(provisions)
    m = len(commandes)

    matrice_transfert = [[0 for _ in range(m)] for _ in range(n)]

    i = j = 0
    while i < n and j < m:
        transfert = min(provisions[i], commandes[j])
        matrice_transfert[i][j] = transfert
        provisions[i] -= transfert
        commandes[j] -= transfert
        if provisions[i] == 0:
            i += 1
        if commandes[j] == 0:
            j += 1

    return matrice_transfert

def afficher_matrice_transfert(matrice_transfert):
    print("Résultat de la méthode du coin nord-ouest :")
    for ligne in matrice_transfert:
        print("[", end="")
        for element in ligne:
            print(f"{element:4}", end=" ")
        print("]")

def balas_hammer(matrice_des_couts, matrice_des_prop, capacites):
    penalites_lignes = [sorted(ligne)[:2] for ligne in matrice_des_couts[:-1]]
    penalites_lignes = [penalites[1] - penalites[0] for penalites in penalites_lignes]

    penalites_colonnes = [sorted(colonne)[:2] for colonne in zip_longest(*matrice_des_couts, fillvalue=0)][:-1]
    penalites_colonnes = [penalites[1] - penalites[0] for penalites in penalites_colonnes]

    max_penalite_ligne = max(penalites_lignes)
    max_penalite_colonne = max(penalites_colonnes)

    if max_penalite_ligne > max_penalite_colonne:
        penalites_type = "ligne"
        indice = penalites_lignes.index(max_penalite_ligne)
        max_penalite = max_penalite_ligne
    elif max_penalite_ligne < max_penalite_colonne :
        penalites_type = "colonne"
        indice = penalites_colonnes.index(max_penalite_colonne)
        max_penalite = max_penalite_colonne
    else:
        indices_lignes_max = [i for i, p in enumerate(penalites_lignes) if p == max_penalite_ligne]
        indices_colonnes_max = [i for i, p in enumerate(penalites_colonnes) if p == max_penalite_colonne]
        if all(p == max_penalite_ligne for p in penalites_lignes):
            penalites_type = "ligne"
            indice = penalites_lignes.index(max_penalite_ligne)
        elif all(p == max_penalite_colonne for p in penalites_colonnes):
            penalites_type = "colonne"
            indice = penalites_colonnes.index(max_penalite_colonne)
        else:
            penalites_type = "ligne" if max_penalite_ligne > max_penalite_colonne else "colonne"
            indice = indices_lignes_max[0] if penalites_type == "ligne" else indices_colonnes_max[0]
        max_penalite = max_penalite_ligne if penalites_type == "ligne" else max_penalite_colonne

    if penalites_type == "ligne":
        arete = [indice, matrice_des_prop[-2].index(min(matrice_des_prop[-2]))]
    else:
        arete = [matrice_des_prop.index(min(matrice_des_prop[:-1], key=lambda x: x[indice])),
                 indice]

    print(f"Pénalité maximale de valeur {max_penalite} située en {penalites_type} {indice}.")

    if matrice_des_prop[arete[0]][arete[1]] == max_penalite:
        print("Il y a plusieurs endroits avec la même valeur de pénalité maximale.")

    quantite_max = min(capacites[arete[0]], capacites[arete[1]])
    print(f"Remplir l'arête {arete} avec une quantité maximale de {quantite_max}")

    capacites[arete[0]] -= quantite_max
    capacites[arete[1]] -= quantite_max
