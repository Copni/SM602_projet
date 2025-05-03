from graph import *
from display import *
from maxEK import get_residual_EK

def init_PR(graph, display=False):
    capacity = graph[0]
    flow = graph[1]
    n = len(capacity)
    s = 0
    t = n - 1

    h = [0] * n # Initialisation des hauteurs
    e = [0] * n # Initialisation des excédents

    h[s] = n

    # Initialisation de le fluc et l'éxédent initial depuis la source
    for v in range(n):
        if capacity[s][v] > 0:
            flow[s][v] = capacity[s][v]
            flow[v][s] = -capacity[s][v] # flot inverse dans le graphe de flot
            e[v] = capacity[s][v]
            e[s] -= capacity[s][v] # exédent retiré de la source
    if display:
        print("Initialisation du flot et de l'exédent :")
        print_heights_and_excess(h, e)
    return h, e


def push_PR(u, v, graph, h, e, display=False):
    capacity = graph[0]
    flow = graph[1]

    residual = capacity[u][v] - flow[u][v] # capacité résiduelle (ce qui peut encore être envoyé)
    if e[u] > 0 and residual > 0 and h[u] == h[v] + 1: # Si exédent et capacité résiduelle, et si la hauteur est valide
        # Mise à jour des flots
        delta = min(e[u], residual)
        flow[u][v] += delta
        flow[v][u] -= delta  # flot inverse dans le graphe de flot
        e[u] -= delta
        e[v] += delta

        if display:
            label_u = "S" if u == 0 else "T" if u == len(h) - 1 else chr(ord('a') + u - 1)
            label_v = "S" if v == 0 else "T" if v == len(h) - 1 else chr(ord('a') + v - 1)
            print(f"Flot poussé de {label_u} vers {label_v} : {delta}")

def relabel_PR(u, graph, h, e, display=False):
    # On réétiquette le noeud u
    capacity = graph[0]
    flow = graph[1]
    n = len(capacity)

    if e[u] <= 0:
        return

    min_height = float('inf')
    for v in range(n):
        if capacity[u][v] - flow[u][v] > 0:
            min_height = min(min_height, h[v])

    if min_height < float('inf'):
        h[u] = min_height + 1

    if display:
        label = "S" if u == 0 else "T" if u == len(h) - 1 else chr(ord('a') + u - 1)
        print(f"Réétiquetage du noeud {label} : nouvelle hauteur {h[u]}")

def maximize_PR(graph, display=False):
    n = len(graph[0])
    s = 0
    t = n - 1

    h, e = init_PR(graph, display)

    # Unitialisation des noeuds actifs
    active = [u for u in range(n) if u != s and u != t and e[u] > 0]
    i = 0
    while active:
        if display:
            active_labels = ["S" if u == 0 else "T" if u == len(h) - 1 else chr(ord('a') + u - 1) for u in active]
            print(f"--- Iteration {i} ---:")
            print(f"Noeuds actifs : {active_labels}")
        u = active.pop(0)
        pushed = False
        # On essaie de pousser le flot vers les voisins
        for v in range(n):
            old_e_v = e[v]
            push_PR(u, v, graph, h, e, display)
            if e[v] > old_e_v and v != s and v != t and v not in active: # Si le flot a été poussé et que v n'est pas la source ou le puits
                active.append(v) # On ajoute v à la liste des noeuds actifs
            if e[u] == 0: # Si l'exédent de u est nul, on ne peut plus pousser de flot
                pushed = True
                break
        if not pushed: # Si on n'a pas pu pousser de flot, on relabel
            relabel_PR(u, graph, h, e, display)
            active.append(u)
        i += 1
        # On affiche les hauteurs et les exédents
        if display:
            label = "S" if u == 0 else "T" if u == len(h) - 1 else chr(ord('a') + u - 1)
            print(f"Après traitement du nœud {label}:")
            print_heights_and_excess(h, e)

    if display:
        flot_max = sum(graph[1][v][t] for v in range(n))  # Somme des flots entrants dans T
        display_flow(graph)
        print(f"Flot maximal: {flot_max}")

    return graph[1]

# Fonction d'affichage des hauteurs et éxécdents

def print_height(h):
    print("Hauteurs :")
    for i in range(len(h)):
        if i == 0:
            label = "S"
        elif i == len(h) - 1:
            label = "T"
        else:
            label = chr(ord('a') + i - 1)
        print(f"    {label} : hauteur de {label}")
    print()

def print_excess(e):
    print("Exédents :")
    for i in range(len(e)):
        if i == 0:
            label = "S"
        elif i == len(e) - 1:
            label = "T"
        else:
            label = chr(ord('a') + i - 1)
        print(f"    {label} : exédent de {e[i]}")
    print()

def print_heights_and_excess(h, e):
    print(f"{'Noeud:':<15}{'Exédent:':<20}{'Hauteur:':<12}")
    for i in range(len(h)):
        if i == 0:
            label = "S"
        elif i == len(h) - 1:
            label = "T"
        else:
            label = chr(ord('a') + i - 1)
        print(f"{label:<15}{e[i]:<20}{h[i]:<15}")
