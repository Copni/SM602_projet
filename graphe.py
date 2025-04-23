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
        for i in range(len(self.nodeList)):
            for j in range(len(self.nodeList)):
                if self.nodeList[i].get_out_node(j) is not None:
                    print(str(self.nodeList[i].get_out_node(j).capacity), end=" ")
                else:
                    print("0", end=" ")
            print()
