from graph import *
from display import *

# Fonction qui renvoie la matrice d'adjacence du graph résiduel
def get_residual_EK(graph):
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
def get_improving_chain_EK(graph, display=False):
    # On récupère la matrice d'adjacence du graph résiduel
    R = get_residual_EK(graph)
    s = 0  # source
    t = len(R) - 1  # puits
    P = {}  # dictionnaire contenant les noeuds parents

    visited = []  # liste des noeuds visités
    queue = [s]  # liste des noeuds à visiter

    # Parcours en largeur
    if display:
        print("Parcours en largeur du graphe résiduel :")
        print("Queue: S")  # Affichage de la source

    while queue != []:
        node = queue.pop(0)
        visited.append(node)

        for i in range(len(R)):
            if R[node][i] > 0 and i not in visited and i not in queue:
                queue.append(i)
                P[i] = node  # on sauvegarde le noeud parent

        if display:
            # Affichage des nœuds dans la file et leurs prédécesseurs
            queue_labels = []
            predecessors = []
            displayed_predecessors = set()  # Ensemble pour suivre les prédécesseurs déjà affichés
            for q in queue:
                label = "S" if q == 0 else "T" if q == len(R) - 1 else chr(ord('a') + q - 1)
                queue_labels.append(label)
                if q in P and q not in displayed_predecessors:
                    pred_label = "S" if P[q] == 0 else "T" if P[q] == len(R) - 1 else chr(ord('a') + P[q] - 1)
                    predecessors.append(f"Π({label}) = {pred_label}")
                    displayed_predecessors.add(q)  # Marquer ce prédécesseur comme affiché
            print("".join(queue_labels), ";" if predecessors else "", "; ".join(predecessors))

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

def adjust_flow_EK(graph, display=False):
    # On récupère la matrice d'adjacence du graphe résiduel
    R = get_residual_EK(graph)
    s = 0 # source
    t = len(R) - 1 # puits

    # On récupère la chaine améliorante
    chain = get_improving_chain_EK(graph, display)
    if chain == []:
        if display:
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

        if display :
            # Conversion des indices en lettres
            def node_to_label(node):
                if node == 0:
                    return 'S'
                elif node == len(graph[1]) - 1:
                    return 'T'
                else:
                    return chr(ord('a') + node - 1)

            chain_labels = " -> ".join(node_to_label(node) for node in chain)
            print("Chaîne améliorante trouvée :", chain_labels)
            print("Flot envoyé sur la chaîne :", min)


        return True

def maximize_EK(graph, display=False):
    # Cette fonction maximise le flux du graphe
    max = True
    i = 0
    while max != None:
        max = adjust_flow_EK(graph, display)
        i += 1
        if display:
            print("Matrice des flots après " + str(i) + " itération:")
            display_flow(graph)
            print("Flot maximum:", sum(graph[1][0]))



