from graph import *

def init_label(graph):
    C = graph[0]
    label = {}
    n = len(C)
    for i in range(n):
        label[i] = 0
    label[0] = n  # Source a hauteur n
    return label


def push(graph, label):
    C = graph[0]
    F = graph[1]
    n = len(C)

    active_nodes = []
    for u in range(1, n-1):  # Ignore source (0) et puits (n-1)
        excess = sum(F[i][u] for i in range(n)) - sum(F[u][j] for j in range(n)) # On calcule l'excès de flot
        if excess > 0:
            active_nodes.append(u) # On ajoute le noeud actif à la liste si il a un excès de flot

    active_nodes.sort()

    for u in active_nodes:
        excess = sum(F[i][u] for i in range(n)) - sum(F[u][j] for j in range(n))
        for v in range(n):
            # Vérifie si une poussée est possible : il doit y avoir de la capacité résiduelle
            # et la hauteur du noeud courant doit être égale à celle du noeud voisin + 1
            if C[u][v] - F[u][v] > 0 and label[u] == label[v] + 1:
                # Calcule le flot maximum pouvant être poussé
                delta = min(excess, C[u][v] - F[u][v])
                # Met à jour le flot dans la direction u -> v
                F[u][v] += delta
                # Met à jour le flot dans la direction inverse v -> u
                F[v][u] -= delta
                return True  # Poussée effectuée
    return False  # Aucune poussée possible


def adjust_label(graph, label):
    C = graph[0]
    F = graph[1]
    n = len(C)

    active_nodes = []
    for u in range(1, n-1):  # Ignore source (0) et puits (n-1)
        excess = sum(F[i][u] for i in range(n)) - sum(F[u][j] for j in range(n))
        if excess > 0:
            active_nodes.append(u)

    active_nodes.sort()

    for u in active_nodes:
        min_height = float('inf')
        for v in range(n):
            if C[u][v] - F[u][v] > 0:
                if label[v] < min_height:
                    min_height = label[v]
        if min_height < float('inf'):
            label[u] = min_height + 1
            break  # Réétiqueter un seul noeud actif
    return label


def maximizePR(graph, display=False):
    label = init_label(graph)
    C = graph[0]
    F = graph[1]
    n = len(C)

    # Pré-flot initial : pousser au maximum depuis la source
    for v in range(1, n):
        if C[0][v] > 0:
            F[0][v] = C[0][v]
            F[v][0] = -C[0][v]

    while True:
        pushed = push(graph, label)
        if not pushed:
            old_label = label.copy()
            label = adjust_label(graph, label)
            if label == old_label:
                break

    graph[1] = convert_flow(F)  # Convertir le flot pour l'affichage
    if display:
        print("Flot maximal :", sum(F[0][j] for j in range(n)))



def convert_flow(F):
    n = len(F)

    final_flow = []
    for i in range(n):
        row = []
        for j in range(n):
            # Si le flot est positif de i vers j, on le garde, sinon 0
            row.append(max(F[i][j], 0))
        final_flow.append(row)

    return final_flow
