from graph import *
from maxFF import get_residualFF

# Fonction qui renvoie la matrice d'adjacence du graph résiduel et sa matrice de coût
def get_residualC(graph):
    R = get_residualFF(graph)
    C = graph[2]

    RC = [[0] * len(R) for _ in range(len(R))]

    for i in range(len(R)):
        for j in range(len(R)):
            if R[i][j] > 0:
                if graph[0][i][j] > 0:  # arc direct
                    RC[i][j] = C[i][j]
                else:  # arc de retour
                    RC[i][j] = -C[j][i]

    return [R, RC]



# Fonction qui retourne la la chaine améliorante d'un graphe en utilisant l'algorithme de Bellman
# Le chemin retourné est une liste contenant les indices des noeuds traversés
def get_improving_chainC(graph, display=False):
    # On récupère la matrice de capacité résiduelle et la matrice de coût résiduel
    R, RC = get_residualC(graph)

    n = len(R)  # nombre de noeuds
    s = 0       # source
    t = n - 1   # puits

    # Initialisation :
    dist = [float('inf')] * n  # distance minimale depuis la source
    dist[s] = 0                # distance de la source à elle-même est 0
    parent = {s: None}         # dictionnaire des parents pour reconstruire le chemin

    # Algorithme de Bellman-Ford (relaxation n-1 fois)
    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if R[u][v] > 0:  # s'il existe un arc résiduel de u vers v
                    if dist[u] + RC[u][v] < dist[v]:
                        dist[v] = dist[u] + RC[u][v]
                        parent[v] = u

    if display:
        print("Distances:", dist)
        print("Parents:", parent)

    # Si le puits n'a pas été atteint, pas de chemin améliorant
    if t not in parent:
        return []

    # Reconstruction du chemin améliorant
    path = []
    current = t
    while current is not None:
        path.append(current)
        current = parent.get(current)

    path.reverse()  # le chemin a été reconstruit à l'envers

    return path


def adjust_flowC(graph, display=False):
    # On récupère la matrice résiduelle et les coûts résiduels
    R, RC = get_residualC(graph)
    s = 0  # source
    t = len(R) - 1  # puits

    # On récupère une chaîne améliorante à coût minimal avec Bellman-Ford
    chain = get_improving_chainC(graph, display)

    if chain == []:
        print("Pas de chaine améliorante")
        return None
    else:
        if display:
            print("Chaîne améliorante trouvée :", chain)

        # Trouver le flot maximum que l'on peut envoyer sur ce chemin
        min_capacity = R[chain[0]][chain[1]]
        for i in range(len(chain) - 1):
            u = chain[i]
            v = chain[i + 1]
            if R[u][v] < min_capacity:
                min_capacity = R[u][v]

        if display:
            print("Flot envoyé sur la chaîne :", min_capacity)

        # Mettre à jour le flux sur le graphe initial
        for i in range(len(chain) - 1):
            u = chain[i]
            v = chain[i + 1]
            # Si l'arc existe dans le graphe original
            if graph[0][u][v] > 0:
                graph[1][u][v] += min_capacity
            else:
                # Sinon, c'est un arc de retour -> on réduit le flux
                graph[1][v][u] -= min_capacity

        return True

def minimizeC(graph, display=False):
    # Cette fonction ajuste le flux pour minimiser le coût total

    improved = True  # Tant qu'on trouve une chaîne améliorante, on continue
    iteration = 0    # Compteur d'itérations

    while improved is not None:
        improved = adjust_flowC(graph, display)
        iteration += 1

        if display:
            print(f"Matrice des flots après l'itération {iteration}:")
            print_matrix(graph[1])
            print()

    if display:
        print("Flot final à coût minimal obtenu.")



