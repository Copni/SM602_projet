from node import *

class Graph:
    def get_node(self, id):
        for i in self.nodeList:
            if i.id == id:
                return i
        print(f"Node {id} not found")
        return None


    def display_data(self):
        for i in self.nodeList:
            i.display()


    def __init__(self, name, file=None):
        self.name = str(name)
        self.nodeList = []  # Liste des nœuds

        if file is not None:
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

                # On vérifit la présence d'une seconde matrice de coût
                if len(lines) == 2 * n:
                    # On assigne les coûts
                    for i in range(n,2*n):
                        for j in range(n):
                            self.nodeList[i-n].get_out_node(j).cost = lines[i][j]
                            self.nodeList[j].get_in_node(i-n).cost = lines[i][j]
        else:
            # Création  d'un graphe vide
            pass


    def get_residual_matrix(self):
        n = len(self.nodeList)
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(len(n)):
                out_node = self.nodeList[i].get_out_node(j)
                if out_node is not None:
                    matrix[i][j] = out_node.capacity - out_node.quantity
        return matrix


    def get_residual_graph(self):
        residual_graph = Graph("R_" + self.name)

        residual_matrix = self.get_residual_matrix()
        n = len(residual_matrix)

        for i in range(n):
            node = Node(i)
            residual_graph.nodeList.append(node)

        # On crée les arcs
        for i in range(n):
            for j in range(n):
                if residual_matrix[i][j] != 0:
                    residual_graph.nodeList[i].outFlow.append(Flow(residual_graph.get_node(j), quantity=(residual_matrix[i][j])))
                    residual_graph.nodeList[j].inFlow.append(Flow(residual_graph.get_node(i), quantity=(residual_matrix[i][j])))


    def width_route(self, display=False):
        queue = [self.get_node(0)]
        visited = []

        while queue:
            node = queue.pop(0)
            visited.append(node)

            if display:
                print(f"\nTête de file : {node.id}")
                print("Noeud en attente: ", ", ".join(str(n.id) for n in queue))

            for flow in node.outFlow:
                if flow.node not in visited and flow.node not in queue:
                    queue.append(flow.node)

        if display:
            print("\nChemin parcouru: ", " -> ".join(str(n.id) for n in visited))

        return visited


    def max_flow(self, display=False):
        # Implémentation de l'algorithme de Ford-Fulkerson
        pass

    def bellman_ford(self, start_node):
        pass








    ### Fonctions d'affichage

    def display_residual(self):
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
        residual_matrix = [[0 for _ in range(n)] for _ in range(n)]

        # Calcul de la matrice résiduelle
        for i in range(n):
            for j in range(n):
                out_node = self.nodeList[i].get_out_node(j)
                if out_node is not None:
                    residual_matrix[i][j] = out_node.capacity - out_node.quantity

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
                label = chr(96 + j)
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
                label = chr(96 + i)
            row = f"{vertical}{label:^{cell_width}}{vertical}"
            for j in range(n):
                residual = residual_matrix[i][j]
                row += f"{residual if residual != 0 else ' ':^{cell_width}}{vertical}"
            print(row)
            if i < n - 1:
                print(separator)
            else:
                # Bas du tableau
                footer = f"{corner_bl}{horizontal * cell_width}{t_up}" + f"{horizontal * cell_width}{t_up}" * (
                            n - 1) + f"{horizontal * cell_width}{corner_br}"
                print(footer)

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

    def display_cost(self):
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
                cost= self.nodeList[i].get_out_node(j).cost if self.nodeList[i].get_out_node(
                    j) is not None else 0
                row += f"{cost if cost != 0 else ' ':^{cell_width}}{vertical}"
            print(row)
            if i < n - 1:
                print(separator)
            else:
                # Bas du tableau
                footer = f"{corner_bl}{horizontal * cell_width}{t_up}" + f"{horizontal * cell_width}{t_up}" * (
                        n - 1) + f"{horizontal * cell_width}{corner_br}"
                print(footer)


