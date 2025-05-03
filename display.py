from graph import *

def display_matrix(matrix):
    row_length = len(matrix[0])
    cell_width = 8

    # En-tête
    header = f"┌{'─' * cell_width}┬" + f"{'─' * cell_width}┬" * (row_length - 1) + f"{'─' * cell_width}┐"
    print(header)

    # Ligne avec les labels de colonnes
    header = f"│{'':^{cell_width}}│"
    for j in range(row_length):
        label = "S" if j == 0 else "T" if j == row_length - 1 else chr(96 + j)
        header += f"{label:^{cell_width}}│"
    print(header)

    # Séparateur
    separator = f"├{'─' * cell_width}┼" + f"{'─' * cell_width}┼" * (row_length - 1) + f"{'─' * cell_width}┤"
    print(separator)

    # Contenu du tableau
    for idx, row in enumerate(matrix):
        label = "S" if idx == 0 else "T" if idx == len(matrix) - 1 else chr(96 + idx)
        row_display = f"│{label:^{cell_width}}│"
        for i in row:
            row_display += f"{str(i).center(cell_width) if i != 0 else ' ' * cell_width}│"
        print(row_display)
        if idx < len(matrix) - 1:
            print(separator)
        else:
            # Bas du tableau
            footer = f"└{'─' * cell_width}┴" + f"{'─' * cell_width}┴" * (row_length - 1) + f"{'─' * cell_width}┘"
            print(footer)


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


def display_flow(graph):
    horizontal = "─"
    vertical = "│"
    corner_tl = "┌"
    corner_tr = "┐"
    corner_bl = "└"
    corner_br = "┘"
    t_down = "┬"
    t_up = "┴"
    t_right = "├"
    t_left = "┤"
    cross = "┼"

    C, F = graph[0], graph[1]  # matrices de capacité et de flux
    n = len(C)
    cell_width = 8

    # En-tête
    header = f"{corner_tl}{horizontal * cell_width}{t_down}" + f"{horizontal * cell_width}{t_down}" * (n - 1) + f"{horizontal * cell_width}{corner_tr}"
    print(header)

    # Ligne avec les labels de colonnes
    header = f"{vertical}{'':^{cell_width}}{vertical}"
    for j in range(n):
        label = "S" if j == 0 else "T" if j == n - 1 else chr(96 + j)
        header += f"{label:^{cell_width}}{vertical}"
    print(header)

    # Séparateur
    separator = f"{t_right}{horizontal * cell_width}{cross}" + f"{horizontal * cell_width}{cross}" * (n - 1) + f"{horizontal * cell_width}{t_left}"
    print(separator)

    # Contenu du tableau
    for i in range(n):
        label = "S" if i == 0 else "T" if i == n - 1 else chr(96 + i)
        row = f"{vertical}{label:^{cell_width}}{vertical}"
        for j in range(n):
            if C[i][j] > 0:
                flow = F[i][j]
                capacity = C[i][j]
                cell_content = f"{flow}/{capacity}"
                row += f"{cell_content:^{cell_width}}{vertical}"
            else:
                row += f"{' ':^{cell_width}}{vertical}"
        print(row)
        if i < n - 1:
            print(separator)
        else:
            # Bas du tableau
            footer = f"{corner_bl}{horizontal * cell_width}{t_up}" + f"{horizontal * cell_width}{t_up}" * (n - 1) + f"{horizontal * cell_width}{corner_br}"
            print(footer)


def display_graph(graph):
    C, F = graph[0], graph[1]  # matrices de capacité et de flux
    n = len(C)
    if len(graph) > 2 and graph[2] != []:
        W = graph[2]  # matrice de coût

    # Symboles pour l'affichage des matrices
    horizontal = '─'
    vertical = '│'
    top_left = '┌'
    top_right = '┐'
    bottom_left = '└'
    bottom_right = '┘'
    cross = '┼'
    left_t = '├'
    right_t = '┤'
    top_t = '┬'
    bottom_t = '┴'
    space = " " * 8  # Espacement entre les matrices

    def build_matrix(matrix, title):
        lines = []
        lines.append(f"{title}:")
        header = f"{top_left}" + f"{horizontal * 3}{top_t}" * (n - 1) + f"{horizontal * 3}{top_right}"
        lines.append(header)

        for i, row in enumerate(matrix):
            row_str = f"{vertical}" + "".join(f"{val:^3}{vertical}" for val in row)
            lines.append(row_str)

            if i < n - 1:
                separator = f"{left_t}" + f"{horizontal * 3}{cross}" * (n - 1) + f"{horizontal * 3}{right_t}"
                lines.append(separator)

        footer = f"{bottom_left}" + f"{horizontal * 3}{bottom_t}" * (n - 1) + f"{horizontal * 3}{bottom_right}"
        lines.append(footer)
        return lines

    # Ajustement des espaces
    esp = " " * 8
    if n > 5:
        esp = esp + " " * (n - 5) * 2

    # Génération des matrices formatées
    capacity_text = build_matrix(C, esp + "Matrice de capacité")
    flow_text = [" " * 8 + line for line in build_matrix(F, "Matrice de flux")]

    if len(graph) > 2 and graph[2] != []:
        cost_text = [" " * 16 + line for line in build_matrix(W, "Matrice de coût")]
        # Affichage des trois matrices côte à côte
        print("\n".join(f"{c_line}{space}{f_line}{space}{cost_line}"
                        for c_line, f_line, cost_line in zip(capacity_text, flow_text, cost_text)))
    else:
        # Affichage de deux matrices côte à côte
        print("\n".join(f"{c_line}{space}{f_line}"
                        for c_line, f_line in zip(capacity_text, flow_text)))
