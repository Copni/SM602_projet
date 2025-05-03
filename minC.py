from graph import *
from display import *
from maxEK import get_residual_EK

# Fonction cherhcant le chemiin de coût minimal depuis la matrice résiduelle
def get_minimal_chain(graph, display=False):
    C, F, cost = graph
    n = len(C)
    R = get_residual_EK(graph)
    s, t = 0, n - 1

    dist = [float('inf')] * n
    pred = [-1] * n
    dist[s] = 0

    def label(i):
        return "S" if i == 0 else "T" if i == n - 1 else chr(ord('A') + i - 1)

    def print_header():
        header = f"{'Iteration':^10}|" + "|".join(f"{label(i):^5}" for i in range(n)) + "|"
        sep = "-" * len(header)
        print(sep)
        print(header)
        print(sep)

    def print_row(iteration, dist):
        row = f"{iteration:^10}|" + "|".join(
            f"{(str(dist[i]) if dist[i] != float('inf') else '∞'):^5}" for i in range(n)
        ) + "|"
        print(row)

    if display:
        print_header()
        print_row(0, dist)

    i = 0
    for u in range(n):
        i += 1
        updated = False
        for v in range(n):
            if R[u][v] > 0 and dist[u] + cost[u][v] < dist[v]:
                dist[v] = dist[u] + cost[u][v]
                pred[v] = u
                updated = True
            if F[u][v] > 0 and dist[v] - cost[u][v] < dist[u]:
                dist[u] = dist[v] - cost[u][v]
                pred[u] = v
                updated = True
        if display:
            print_row(i, dist.copy())

        if not updated:
            break

    if display:
        print("-" * (11 + 6 * n))

    if pred[t] == -1:
        if display:
            print("Aucun chemin de coût minimal trouvé.")
        return []

    # Reconstruction du chemin
    chain = []
    node = t
    while node != -1:
        chain.append(node)
        node = pred[node]
    chain.reverse()

    if display:
        path_labels = " -> ".join(label(i) for i in chain)
        print("Chaîne de coût minimal trouvée :", path_labels)
        print("Coût total :", dist[t])

    return chain




def adjust_flow_C(graph, n, display=False):
    R = get_residual_EK(graph)
    C, F, cost = graph
    chain = get_minimal_chain(graph, display)

    if not chain:
        if display:
            print("Aucun chemin disponible.")
        return n  # Aucun flot n'a pu être envoyé

    # Trouver le débit possible sur la chaîne (minimum des capacités résiduelles)
    min_capacity = float('inf')
    for i in range(len(chain) - 1):
        u, v = chain[i], chain[i + 1]
        if C[u][v] > F[u][v]:  # arc direct
            capacity = C[u][v] - F[u][v]
        else:  # arc inverse
            capacity = F[v][u]
        if capacity < min_capacity:
            min_capacity = capacity

    flow_to_send = min(n, min_capacity)

    # Mettre à jour les flux
    for i in range(len(chain) - 1):
        u, v = chain[i], chain[i + 1]
        if C[u][v] > F[u][v]:  # arc direct
            F[u][v] += flow_to_send
        else:  # arc inverse
            F[v][u] -= flow_to_send

    if display:
        print("Matrice résiduelle mise à jour :")
        display_matrix(R)
        labels = lambda i: "S" if i == 0 else "T" if i == len(F) - 1 else chr(ord('a') + i - 1)
        print("Flot envoyé sur la chaîne :", flow_to_send)
        print("Chaîne utilisée :", " -> ".join(labels(i) for i in chain))

    return n - flow_to_send


def minimize_C(graph, n, display=False):
    remaining = n
    iteration = 1

    while remaining > 0:
        if display:
            print()
            print(f"--- Itération {iteration} ---")

        previous = remaining
        remaining = adjust_flow_C(graph, remaining, display)
        sent = previous - remaining
        iteration += 1

        if sent == 0:
            if display:
                print("Plus de chemin disponible. Flot partiellement envoyé.")
            break

    total_sent = n - remaining
    total_cost = 0
    C, F, cost = graph

    for i in range(len(C)):
        for j in range(len(C)):
            total_cost += F[i][j] * cost[i][j]

    print(f"Flot total envoyé : {total_sent}/{n}")
    print(f"Coût total du flot : {total_cost}")


