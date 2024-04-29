import os
import random


def choisir_fichier(dossier):
    fichiers = os.listdir(dossier)
    print("Liste des problèmes de transport dans le dossier :")
    for fichier in fichiers:
        print(fichier)
    nom_fichier = input("Entrez le nom du fichier que vous voulez afficher : ")
    return nom_fichier


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


def afficher_matrice_nordouest(matrice_transfert):
    print("Résultat de la méthode du coin nord-ouest :")
    for ligne in matrice_transfert:
        print("[", end="")
        for element in ligne:
            print(f"{element:4}", end=" ")
        print("]")


def balas_hammer(matrice_des_couts, matrice_des_prop, capacites,):
    provisions = [ligne[-1] for ligne in matrice_des_prop[:-1]]
    commandes = matrice_des_prop[-1]
    n = len(provisions)
    m = len(commandes)
    matrice_transfert = [[0] * m for _ in range(n)]
    cout_total = 0

    # Calculez les pénalités pour chaque ligne et chaque colonne
    penalties = []
    for i in range(n):
        row = sorted(matrice_des_couts[i])
        if len(row) > 1:
            penalties.append((row[1] - row[0], 'row', i))
    for j in range(m):
        col = sorted([matrice_des_couts[i][j] for i in range(n)])
        if len(col) > 1:
            penalties.append((col[1] - col[0], 'col', j))

    # Triez et trouvez la pénalité maximale
    penalties.sort(reverse=True, key=lambda x: x[0])
    max_penalty = penalties[0][0]

    # Identifiez toutes les pénalités maximales
    max_penalties = [p for p in penalties if p[0] == max_penalty]

    # Afficher les informations sur les pénalités maximales
    print(f"Pénalité maximale de {max_penalty} trouvée en :")
    for penalty in max_penalties:
        if penalty[1] == 'row':
            print(f" - Ligne {penalty[2]}")
        else:
            print(f" - Colonne {penalty[2]}")

    # Sélection aléatoire parmi les pénalités maximales si plusieurs
    if len(max_penalties) > 1:
        selected_penalty = random.choice(max_penalties)
        print("Plusieurs emplacements pour la pénalité maximale ont été détectés.")
        print(f"Choix aléatoire : {'Ligne' if selected_penalty[1] == 'row' else 'Colonne'} {selected_penalty[2]}")
    else:
        selected_penalty = max_penalties[0]

    p_type, idx = selected_penalty[1], selected_penalty[2]

    # Déterminez l'arête à remplir
    if p_type == 'row':
        min_cost_index = matrice_des_couts[idx].index(min(matrice_des_couts[idx]))
        quantity_to_fill = min(provisions[idx], commandes[min_cost_index])
        print(f"Remplir l'arête ({idx}, {min_cost_index}) avec la quantité {quantity_to_fill}.")
        matrice_transfert[idx][min_cost_index] += quantity_to_fill
    elif p_type == 'col':
        min_cost_index = [matrice_des_couts[i][idx] for i in range(n)].index(min([matrice_des_couts[i][idx] for i in range(n)]))
        quantity_to_fill = min(provisions[min_cost_index], commandes[idx])
        print(f"Remplir l'arête ({min_cost_index}, {idx}) avec la quantité {quantity_to_fill}.")
        matrice_transfert[min_cost_index][idx] += quantity_to_fill

    return matrice_transfert, cout_total