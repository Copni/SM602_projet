from node import Node

from graph import Graph

def main():
    # Create a graph
    graph = Graph("TestGraph", "proposition1.txt")

    # Display the graph
    graph.display_data()

    graph.display_capacity()
    graph.display_cost()
    graph.display_residual()
    print()
    graph.width_route(display=True)


if __name__ == "__main__":
    main()
