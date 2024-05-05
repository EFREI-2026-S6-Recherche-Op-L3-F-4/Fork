import os
import random
from collections import deque
from prettytable import PrettyTable

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


def afficher_matrice_transfert(matrice_transfert):
    table = PrettyTable()

    # Définir les noms de colonnes
    table.field_names = [" "] + [f"C{i+1}" for i in range(len(matrice_transfert[0]))]

    # Ajouter les lignes avec les noms de lignes
    for i, ligne in enumerate(matrice_transfert):
        table.add_row([f"S{i+1}"] + ligne)

    print(table)


def balas_hammer(matrice_des_couts, matrice_des_prop):
    provisions = [ligne[-1] for ligne in matrice_des_prop[:-1]]
    commandes = matrice_des_prop[-1]
    n = len(provisions)
    m = len(commandes)

    if sum(provisions) != sum(commandes):
        print("Problème non équilibré, nous ne pouvons pas appliquer Balas-Hammer")
        return None

    matrice_transfert = [[0] * m for _ in range(n)]

    while any(provisions) and any(commandes):  # Continue tant qu'il y a des provisions et des commandes non nulles
        penalties = []
        for i in range(n):
            if provisions[i] > 0:
                active_costs = [(matrice_des_couts[i][j], j) for j in range(m) if commandes[j] > 0]
                if len(active_costs) > 1:
                    sorted_costs = sorted(active_costs)
                    penalty_value = sorted_costs[1][0] - sorted_costs[0][0]
                    penalties.append((penalty_value, 'row', i, sorted_costs[0][0], provisions[i], sorted_costs[0][1]))
        for j in range(m):
            if commandes[j] > 0:
                active_costs = [(matrice_des_couts[i][j], i) for i in range(n) if provisions[i] > 0]
                if len(active_costs) > 1:
                    sorted_costs = sorted(active_costs)
                    penalty_value = sorted_costs[1][0] - sorted_costs[0][0]
                    penalties.append((penalty_value, 'col', j, sorted_costs[0][0], commandes[j], sorted_costs[0][1]))

        if not penalties:  # Si pas de pénalités calculables, forcer le traitement
            for i in range(n):
                for j in range(m):
                    if provisions[i] > 0 and commandes[j] > 0:
                        transfer = min(provisions[i], commandes[j])
                        matrice_transfert[i][j] += transfer
                        provisions[i] -= transfer
                        commandes[j] -= transfer
            continue

        penalties.sort(key=lambda x:
(-x[0], x[3]))  # Trier par pénalité maximale, puis par coût minimal
        chosen_penalty = penalties[0]
        _, p_type, idx, _, _, min_cost_idx = chosen_penalty

        # Effectuer le transfert
        if p_type == 'row':
            quantity_to_fill = min(provisions[idx], commandes[min_cost_idx])
            matrice_transfert[idx][min_cost_idx] += quantity_to_fill
            provisions[idx] -= quantity_to_fill
            commandes[min_cost_idx] -= quantity_to_fill
        else:
            quantity_to_fill = min(provisions[min_cost_idx], commandes[idx])
            matrice_transfert[min_cost_idx][idx] += quantity_to_fill
            provisions[min_cost_idx] -= quantity_to_fill
            commandes[idx] -= quantity_to_fill

        print(f"Choix final pour maximiser l'efficacité : {'Ligne' if p_type == 'row' else 'Colonne'} {idx}, quantité {quantity_to_fill} transférée")

    return matrice_transfert

def calculer_cout_total(matrice_des_couts, matrice_transfert):
    n = len(matrice_transfert)    # Nombre de lignes
    m = len(matrice_transfert[0]) # Nombre de colonnes

    cout_total = 0
    for i in range(n):
        for j in range(m):
            cout_total += matrice_des_couts[i][j] * matrice_transfert[i][j]

    return cout_total
def detecter_cycle(matrice_transfert):
    n = len(matrice_transfert)  # Nombre de lignes
    m = len(matrice_transfert[0])  # Nombre de colonnes

    # Créer le graphe des transferts (uniquement les liens unidirectionnels ligne -> colonne)
    graphe = {i: [] for i in range(n + m)}  # n pour les lignes, m pour les colonnes

    for i in range(n):
        for j in range(m):
            if matrice_transfert[i][j] > 0:
                # Ajoute une arête de la ligne i à la colonne j (dans les colonnes, décalé de n)
                graphe[i].append(j + n)

    visite = [False] * (n + m)
    recursion_stack = [False] * (n + m)

    def dfs(v):
        if not visite[v]:
            visite[v] = True
            recursion_stack[v] = True
            for voisin in graphe[v]:
                if not visite[voisin] and dfs(voisin):
                    return True
                elif recursion_stack[voisin]:
                    return True
        recursion_stack[v] = False
        return False

    for i in range(n + m):
        if not visite[i] and dfs(i):
            print("Un cycle est détecté dans la matrice de transfert.")
            return True

    print("Aucun cycle détecté dans la matrice de transfert.")
    return False

def maximiser_transport(matrice_transfert, matrice_des_couts):
    n = len(matrice_transfert)
    m = len(matrice_transfert[0])

    # Supposons que la fonction detecter_cycle retourne les indices formant un cycle si détecté
    cycle = detecter_cycle(matrice_transfert)  # Cette fonction devrait retourner les indices du cycle
    if not cycle:
        print("Aucun cycle à maximiser.")
        return

    print("Cycle détecté, maximisation en cours...")
    # Trouver le coût minimal et maximal dans le cycle
    min_cost = float('inf')
    max_cost = 0
    for (i, j) in cycle:
        if matrice_des_couts[i][j] < min_cost:
            min_cost = matrice_des_couts[i][j]
            min_edge = (i, j)
        if matrice_des_couts[i][j] > max_cost:
            max_cost = matrice_des_couts[i][j]
            max_edge = (i, j)

    # Afficher les conditions pour chaque case du cycle
    for (i, j) in cycle:
        print(f"Arête ({i}, {j}) avec coût {matrice_des_couts[i][j]} et transport {matrice_transfert[i][j]}")
    ajustement = min(matrice_transfert[max_edge[0]][max_edge[1]], matrice_transfert[min_edge[0]][min_edge[1]])
    matrice_transfert[max_edge[0]][max_edge[1]] -= ajustement
    matrice_transfert[min_edge[0]][min_edge[1]] += ajustement

    print(f"Arête supprimée ou ajustée : {max_edge} pour maximiser le coût.")

def verifier_connexite(matrice_transfert):
    n = len(matrice_transfert)
    m = len(matrice_transfert[0])
    visite = [False] * (n + m)  # n lignes + m colonnes


    def bfs(start):
        queue = deque([start])
        composante = []
        while queue:
            node = queue.popleft()
            if not visite[node]:
                visite[node] = True
                composante.append(node)
                # Ajoutez tous les nœuds connectés à ce nœud dans la queue
                if node < n:  # C'est une ligne
                    for j in range(m):
                        if matrice_transfert[node][j] > 0 and not visite[j + n]:
                            queue.append(j + n)
                else:  # C'est une colonne
                    for i in range(n):
                        if matrice_transfert[i][node - n] > 0 and not visite[i]:
                            queue.append(i)
        return composante

    composantes = []
    for i in range(n + m):
        if not visite[i]:
            comp = bfs(i)
            if comp:
                # Remplacer les chiffres par S1, S2, etc. et C1, C2, etc.
                comp = ['S' + str(c + 1) if c < n else 'C' + str(c - n + 1) for c in comp]
                composantes.append(comp)




    if len(composantes) == 1:
        print("La matrice de transfert est connexe.")
    else:
        print("La matrice de transfert est non connexe. Voici les sous-graphes connexes composant la proposition:")
        for i, comp in enumerate(composantes):
            print(comp, end=',' if i < len(composantes) - 1 else '\n')


