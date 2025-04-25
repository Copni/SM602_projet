from node import *

class Graph:
    def get_node(self, id):
        for i in self.nodeList:
            if i.id == id:
                return i
        print(f"Node {id} not found")
        return None


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
            for j in range(n):
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

        return residual_graph

    def width_route(self, display=False):
        start_node = self.get_node(0)
        final_node_id = len(self.nodeList) - 1
        queue = [start_node]
        visited = []
        # Dictionnaire pour stocker le parent de chaque nœud
        parent = {start_node: None}

        while queue:
            node = queue.pop(0)
            visited.append(node)

            if display:
                print(f"\nTête de file : {node.id}")
                print("Noeud en attente: ", ", ".join(str(n.id) for n in queue))

            if node.id == final_node_id:
                # Reconstruction du chemin
                path = []
                current = node
                while current is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()

                if display:
                    print("\nChemin trouvé: ", " -> ".join(str(n.id) for n in path))
                return path

            # Trier les flux sortants par id de nœud croissant
            sorted_flows = sorted(node.outFlow, key=lambda x: x.node.id)
            for flow in sorted_flows:
                if flow.node not in visited and flow.node not in queue:
                    queue.append(flow.node)
                    parent[flow.node] = node

        return None  # Si aucun chemin n'est trouvé


    def maximize_flow(self, display=False):
        # Implémentation de l'algorithme de Ford-Fulkerson

        # On crée le graphe résiduel
        residual_graph = self.get_residual_graph()

        # On parcourt le graphe résiduel en largeur et on récupère le chemin
        path = residual_graph.width_route()

        # On vérifit que le chemin conduit bien au noeud terminal
        if path[-1].id != len(residual_graph.nodeList) - 1:
            print("On ne peut pas maximiser plus le flot")
            return False
        else: # On maximise le flot de path
            # On cherche le débit optimisable
            print("hello")
            print(path[0].get_out_flow(path[1]).quantity)
            min_quantity = path[0].get_out_flow(path[1]).quantity
            for i in range(len(path) - 1):
                flow = path[i].get_out_flow(path[i + 1])
                if flow and flow.quantity < min_quantity:
                    min_quantity = flow.quantity

                    # On met à jour les capacités du graphe
                    for i in range(len(path) - 1):
                        # Mise à jour du flot direct
                        out_flow = self.nodeList[path[i].id].get_out_flow(self.nodeList[path[i + 1].id])
                        if out_flow:
                            out_flow.quantity += min_quantity

                        # Mise à jour du flot inverse
                        in_flow = self.nodeList[path[i + 1].id].get_in_flow(self.nodeList[path[i].id])
                        if in_flow:
                            in_flow.quantity += min_quantity
            if display:
                print(f"\nFlot maximisé de {min_quantity} entre le noeud {path[0].id} et le noeud {path[-1].id}")
                print("Flot mis à jour: ")
                self.display_residual()
                self.display_quantity()

            return True

    def maximize_graph(self, display=False):
        # On maximise le flot tant qu'il y a un chemin entre S et T
        max = True
        while max != False:
            max = self.maximize_flow(display)







    def bellman_ford(self, start_node):
        pass








    ### Fonctions d'affichage

    def display_data(self):
        for i in self.nodeList:
            i.display()


    def display_residual(self):
        print("Matrice d'adjacence du graphe résiduel :")
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
        print("Matrice de capacités du graphes")
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
        print("Matrice de coût du graphe :")
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

    def display_quantity(self):
        print("Matrice des quantités du graphe :")
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

        # En-tête
        header = f"{corner_tl}{horizontal * cell_width}{t_down}" + f"{horizontal * cell_width}{t_down}" * (
                    n - 1) + f"{horizontal * cell_width}{corner_tr}"
        print(header)

        # Ligne avec les labels de colonnes
        header = f"{vertical}{'':^{cell_width}}{vertical}"
        for j in range(n):
            label = "S" if j == 0 else "T" if j == n - 1 else chr(96 + j)
            header += f"{label:^{cell_width}}{vertical}"
        print(header)

        # Séparateur
        separator = f"{t_right}{horizontal * cell_width}{cross}" + f"{horizontal * cell_width}{cross}" * (
                    n - 1) + f"{horizontal * cell_width}{t_left}"
        print(separator)

        # Contenu du tableau
        for i in range(n):
            label = "S" if i == 0 else "T" if i == n - 1 else chr(96 + i)
            row = f"{vertical}{label:^{cell_width}}{vertical}"
            for j in range(n):
                out_flow = self.nodeList[i].get_out_node(j)
                if out_flow is not None:
                    quantity = out_flow.quantity
                    capacity = out_flow.capacity
                    cell_content = f"{quantity}/{capacity}"
                    row += f"{cell_content:^{cell_width}}{vertical}"
                else:
                    row += f"{' ':^{cell_width}}{vertical}"
            print(row)
            if i < n - 1:
                print(separator)
            else:
                # Bas du tableau
                footer = f"{corner_bl}{horizontal * cell_width}{t_up}" + f"{horizontal * cell_width}{t_up}" * (
                            n - 1) + f"{horizontal * cell_width}{corner_br}"
                print(footer)

