# Fonction initialisant un graphe à partir d'un fichier
# Dans ce programme, un graphe est représenté par une liste contenant trois matrices :
# - la matrice de capacité
# - la matrice de flux
# - la matrice de coût (liste vide si non spécifiée)
def read_graph(file):
    # retourne la matrice de capacité du graph
    with open (file, 'r') as f:
        lines = f.readlines()
        size = int(lines.pop(0))

        # formatage de chaque ligne pour la rendre lisible
        for i in range(len(lines)):
            lines[i] = lines[i].split()
            for j in range(len(lines[i])):
                lines[i][j] = int(lines[i][j])


        # creation de la matrice de capacité
        capacity = []

        for i in range(size):
            row = []
            for j in range(size):
                row.append(lines[i][j])
            capacity.append(row)

        # creation de la matrice des flux
        flow = []
        for i in range(len(capacity)):
            row = []
            for j in range(len(capacity)):
                row.append(0)
            flow.append(row)

        # creation de la matrice de coût
        cost = []
        if len(lines) == 2 * size:
            for i in range(size):
                row = []
                for j in range(size):
                    row.append(lines[i + size][j])
                cost.append(row)

        data = [capacity, flow, cost]
    return data


# Fonction qui affiche une matrice
def print_matrix(matrix):
    for row in matrix:
        for i in row:
            print(i, end=' ')
        print()


# Fonction affichant les matrices de capacité, de flux et de coût associées à un graph
def print_graph(graph):
    # Affiche le graph
    print("Matrice des capacités :")
    print_matrix(graph[0])
    print("Matrice des flots :")
    print_matrix(graph[1])
    if graph[2] != []:
        print("Matrice des coûts :")
        print_matrix(graph[2])
