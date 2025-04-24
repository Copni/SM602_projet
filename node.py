from copy import deepcopy

class Node:
    def __init__(self, id, inFlow=None, outFlow=None):
        self.id = id
        self.inFlow = inFlow if inFlow is not None else []
        self.outFlow = outFlow if outFlow is not None else []

    def duplicate(self, name=None):
        d = deepcopy(self)
        if name is not None:
            d.id = str(name)
        return d

    def display(self):
        print(f"Noeud : {self.id:<10}")
        for i in self.inFlow:
            i.display_data("in")
        for i in self.outFlow:
            i.display_data()
        print()

    def get_out_node(self, id):
        for i in self.outFlow:
            if i.node.id == id:
                return i
        return None

    def get_in_node(self, id):
        for i in self.inFlow:
            if i.node.id == id:
                return i
        return None

class Flow:
    def __init__(self, node, capacity, quantity=0, cost=None):
        self.node =  node
        self.capacity = capacity if capacity is not None else 0
        self.quantity = quantity
        self.cost = cost if cost is not None else 0

    def duplicate(self, name=None):
        d = deepcopy(self)
        return d

    def display(self, direction=None):
        if direction is None or direction == "out":
            print(f"    Destination : {self.node.id:<10} Coût : {self.cost:<10} Capacité : {self.capacity:<10}")
        else :
            if direction == "in":
                print(f"    Source      : {self.node.id:<10} Coût : {self.cost:<10} Capacité : {self.capacity:<10}")
            else:
                print("Erreur d'affichage")
                return None
