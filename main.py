from graph import *
from maxFF import *
from maxPR import *
from minC import minimizeC

'''
graph = read_graph("proposition1.txt")
print_graph(graph)

maximizePR(graph, True)
print_graph(graph)

graph = read_graph("proposition1.txt")
maximizePR(graph, True)
print_graph(graph)
'''
graph = read_graph("P6-flotmin.txt")
minimizeC(graph, True)
