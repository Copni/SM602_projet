from graph import Graph

def main():
    # Create a graph
    graph = Graph("TestGraph", "proposition1.txt")

    # Display the graph
    graph.display_data()

    print()
    graph.width_route(display=True)
    graph.maximize_flow(display=True)
    graph.width_route(display=True)
    graph.maximize_flow(display=True)
    graph.width_route(display=True)
    graph.maximize_flow(display=True)



if __name__ == "__main__":
    main()

