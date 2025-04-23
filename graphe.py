from node import *

class Graphe:
    def get_node(self, id):
        for i in self.nodeList:
            if i.id == id:
                return i
        print(f"Node {id} not found")
        return None

    def display(self):
        for i in self.nodeList:
            i.display()

    def __init__(self, name, file=None):
        self.name = str(name)
        self.nodeList = []  # Liste des nœuds

        with open(file, 'r') as f:
            lines = f.readlines()

            # On récupère le nombre de noeud
            n = int(lines.pop(0))

            # formatage de chaque ligne pour la rendre lisible
            for i in range(len(lines)):
                lines[i] = lines[i].split()
                for j in range(len(lines[i])):
                    lines[i][j] = int(lines[i][j])

            # On crée n noeuds
            for i in range(n):
                node = Node(i)
                self.nodeList.append(node)


            # Affichage de la matrice pour le debug
            for i in range(n):
                for j in range(len(lines[i])):
                    print(lines[i][j], end=" ")
                print()

            # On crée les arcs
            for i in range(n):
                for j in range(len(lines[i])):
                    if lines[i][j] != 0:
                        self.nodeList[i].outFlow.append(Flow(self.get_node(j), int(lines[i][j])))
                        self.nodeList[j].inFlow.append(Flow(self.get_node(i), int(lines[i][j])))

    def display_capacity(self):
        # Caractères box ASCII
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

        n = len(self.nodeList)
        cell_width = 8

        # En-tête avec la première ligne
        header = f"{corner_tl}{horizontal * cell_width}{t_down}" + f"{horizontal * cell_width}{t_down}" * (
                    n - 1) + f"{horizontal * cell_width}{corner_tr}"
        print(header)

        # Ligne avec les numéros de colonnes
        header = f"{vertical}{'':^{cell_width}}{vertical}"
        for j in range(n):
            if j == 0:
                label = "S"
            elif j == n - 1:
                label = "T"
            else:
                label = chr(96 + j)  # 97 est le code ASCII pour 'a'
            header += f"{label:^{cell_width}}{vertical}"
        print(header)

        # Séparateur
        separator = f"{t_right}{horizontal * cell_width}{cross}" + f"{horizontal * cell_width}{cross}" * (
                    n - 1) + f"{horizontal * cell_width}{t_left}"
        print(separator)

        # Contenu du tableau
        for i in range(n):
            if i == 0:
                label = "S"
            elif i == n - 1:
                label = "T"
            else:
                label = chr(96 + i)  # 97 est le code ASCII pour 'a'
            row = f"{vertical}{label:^{cell_width}}{vertical}"
            for j in range(n):
                capacity = self.nodeList[i].get_out_node(j).capacity if self.nodeList[i].get_out_node(
                    j) is not None else 0
                row += f"{capacity if capacity != 0 else ' ':^{cell_width}}{vertical}"
            print(row)
            if i < n - 1:
                print(separator)
            else:
                # Bas du tableau
                footer = f"{corner_bl}{horizontal * cell_width}{t_up}" + f"{horizontal * cell_width}{t_up}" * (
                            n - 1) + f"{horizontal * cell_width}{corner_br}"
                print(footer)
