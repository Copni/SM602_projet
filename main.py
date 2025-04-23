from node import Node

from graphe import Graphe

def main():
    # Create a graph
    graph = Graphe("TestGraph", "proposition1.txt")

    # Display the graph
    graph.display()

    graph.display_capacity()

if __name__ == "__main__":
    main()
