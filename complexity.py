import random
from display import *
from graph import *
from maxEK import *
from maxPR import *
from minC import *
from time import perf_counter

# Fonction pour générer aléatoirement un problème de flot
def create_graph(size, minimisation=False):
    # Initialisation des matrices
    capacity_matrix = [[0] * size for _ in range(size)]
    flow_matrix = [[0] * size for _ in range(size)]
    cost_matrix = [[0] * size for _ in range(size)]

    # Remplissage de la matrice des capacités
    non_zero_count = 0
    total_cells = size * size
    for i in range(size):
        for j in range(size):
            if i != j:  # La diagonale doit rester nulle
                if random.random() > 0.5 and non_zero_count < total_cells // 2:
                    capacity_matrix[i][j] = random.randint(1, 100)
                    if minimisation:
                        cost_matrix[i][j] = random.randint(1, 10)
                    non_zero_count += 1

    # Construction du graph
    graph = [capacity_matrix, flow_matrix, cost_matrix]
    return graph

def create_test_bench(n, size, minimisation=False):
    test_bench = []
    for i in range(n):
        graph = create_graph(size, minimisation)
        test_bench.append(graph)
    return test_bench

def test(n, size, algorithm):
    test_bench = create_test_bench(n, size, minimisation=(algorithm == "minimisation"))
    times = []

    for i, graph in enumerate(test_bench):
        print(f"Test {i + 1}:")
        start_time = perf_counter()
        if algorithm == "EK":
            maximize_EK(graph, display=False)
        elif algorithm == "PR":
            maximize_PR(graph, display=False)
        elif algorithm == "min":
            minimize_C(graph, n=1, display=False)
        else:
            raise ValueError("Algorithme non reconnu : choisissez 'EK', 'PR' ou 'min'.")

        end_time = perf_counter()
        elapsed_time = end_time - start_time
        print(f"Temps écoulé : {elapsed_time:.6f} secondes")
        times.append(elapsed_time)

    return times

def save_results(times, algorithm, size):
    import csv

    filename = f"results_{algorithm}_size{size}.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Test", "Temps (secondes)"])
        for i, time in enumerate(times, start=1):
            writer.writerow([i, time])

    print(f"Résultats sauvegardés dans le fichier {filename}")


test(100, 1000, "EK")



