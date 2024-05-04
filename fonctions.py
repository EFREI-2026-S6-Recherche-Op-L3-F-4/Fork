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
    # Initialisation
    provisions = [ligne[-1] for ligne in matrice_des_prop[:-1]]
    commandes = matrice_des_prop[-1]
    n = len(provisions)
    m = len(commandes)
    # Vérifiez si le problème est équilibré
    if sum(provisions) != sum(commandes):
        print("Problème non équilibré, nous ne pouvons pas appliquer balas hammer")
        return(None, None)
    print("Problème équilibré, nous pouvons appliquer balas hammer")

    matrice_transfert = [[0] * m for _ in range(n)]

    # Calculez les pénalités pour chaque ligne et chaque colonne
    while sum(provisions) > 0 and sum(commandes) > 0:
        penalties = []
        for i in range(n):
            if provisions[i] > 0:
                costs = [matrice_des_couts[i][j] for j in range(m) if commandes[j] > 0]
                if len(costs) > 1:
                    sorted_costs = sorted(costs)
                    penalties.append((sorted_costs[1] - sorted_costs[0], 'row', i))
        for j in range(m):
            if commandes[j] > 0:
                costs = [matrice_des_couts[i][j] for i in range(n) if provisions[i] > 0]
                if len(costs) > 1:
                    sorted_costs = sorted(costs)
                    penalties.append((sorted_costs[1] - sorted_costs[0], 'col', j))
        # Si aucune pénalité n'est trouvée (s'il reste une seule arête par ligne/colonne) , forcer le remplissage
        if not penalties:
            for i in range(n):
                for j in range(m):
                    if provisions[i] > 0 and commandes[j] > 0:
                        matrice_transfert[i][j] += min(provisions[i], commandes[j])
                        provisions[i] -= min(provisions[i], commandes[j])
                        commandes[j] -= min(provisions[i], commandes[j])
                        print(f"Forçage de remplissage: ({i}, {j}) avec la quantité restante.")
            continue

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
            min_cost_index = min((matrice_des_couts[idx][j], j)
                                 for j in range(m) if commandes[j] > 0)[1]
            quantity_to_fill = min(provisions[idx], commandes[min_cost_index])
            print(f"Remplir l'arête ({idx}, {min_cost_index}) avec la quantité {quantity_to_fill}.")
            matrice_transfert[idx][min_cost_index] += quantity_to_fill
            provisions[idx] -= quantity_to_fill
            commandes[min_cost_index] -= quantity_to_fill
        elif p_type == 'col':
            min_cost_index = (min((matrice_des_couts[i][idx], i)
                                  for i in range(n) if provisions[i] > 0))[1]
            quantity_to_fill = min(provisions[min_cost_index], commandes[idx])
            print(f"Remplir l'arête ({min_cost_index}, {idx}) avec la quantité {quantity_to_fill}.")
            matrice_transfert[min_cost_index][idx] += quantity_to_fill
            provisions[min_cost_index] -= quantity_to_fill
            commandes[idx] -= quantity_to_fill

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

        return composantes
