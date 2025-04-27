from graph import *

# Fonction qui renvoie la matrice d'adjacence du graph résiduel
def get_residualFF(graph):
    C = graph[0]  # capacité
    F = graph[1]  # flux
    n = len(C)

    R = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if C[i][j] > F[i][j]:
                R[i][j] = C[i][j] - F[i][j]
            if F[i][j] > 0:
                R[j][i] = F[i][j]

    return R

# Fonction qui retourne la la chaine améliorante d'un graphe en utilisant le parcours en largeur
# Le chemin retourné est une liste contenant les indices des noeuds traversés
def get_improving_chainFF(graph, display=False):
    # On récupère la matrice d'adjacence du graph résiduel
    R = get_residualFF(graph)
    s = 0 # source
    t = len(R) - 1 # puits
    P = {} # dictionnaire contenant les noeuds parents

    visited = [] # liste des noeuds visités
    queue = [s] # liste des noeuds à visiter

    # Parcours en largeur
    while queue != []:

        node = queue.pop(0)
        visited.append(node)

        if display:
            print("Tête de liste:", node)

        for i in range(len(R)):
            if R[node][i] > 0 and i not in visited and i not in queue:
                queue.append(i)
                P[i] = node  # on sauvegarde le noeud parent

        print("Queue:", queue)
        print()

    if t not in visited:
        return []
    else:
        # On remonte la chaine améliorante
        chain = []
        node = t
        while node != s:
            chain.append(node)
            node = P[node]
        chain.append(s)
        chain.reverse()
        return chain

def adjust_flowFF(graph, display=False):
    # On récupère la matrice d'adjacence du graphe résiduel
    R = get_residualFF(graph)
    s = 0 # source
    t = len(R) - 1 # puits

    # On récupère la chaine améliorante
    chain = get_improving_chainFF(graph, display)
    if chain == []:
        print("Pas de chaine améliorante")
        return None
    else:
        # On cherche le minimum de la chaine
        min = R[chain[0]][chain[1]]
        for i in range(len(chain) - 1):
            if R[chain[i]][chain[i + 1]] < min:
                min = R[chain[i]][chain[i + 1]]

        # le min récupéré, on met à jour le flux
        for i in range(len(chain) - 1):
            graph[1][chain[i]][chain[i + 1]] += min
        return True

def maximizeFF(graph, display=False):
    # Cette fonction maximise le flux du graphe
    max = True
    i = 0
    while max != None:
        max = adjust_flowFF(graph, display)
        i += 1
        if display:
            print("Matrice des flux après l'itération", i)
            print_matrix(graph[1])
