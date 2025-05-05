import random
from display import *
from graph import *
from maxEK import *
from maxPR import *
from minC import *
from time import perf_counter
import os
import csv
import matplotlib.pyplot as plt

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
            n = sum(graph[0][i][-1] for i in range(len(graph[0]) - 1)) // 2
            minimize_C(graph, n, display=False)
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

def generate_data(algorithm, n, size):
    times = test(n, size, algorithm)
    # Sauvegarde des résultats
    save_results(times, algorithm, size)


def display_result():
    csv_files = [f for f in os.listdir('.') if f.startswith("results_") and f.endswith(".csv")]

    if not csv_files:
        print("Aucun fichier de résultats trouvé.")
        return

    data = {}

    # Lecture des fichiers CSV
    for file in csv_files:
        parts = file.split('_')
        if len(parts) < 3:
            continue
        algorithm = parts[1]
        size = int(parts[2][4:-4])  # Extraire la taille depuis "sizeX.csv"

        if algorithm not in data:
            data[algorithm] = []

        with open(file, mode="r") as f:
            reader = csv.DictReader(f)
            times = [float(row["Temps (secondes)"]) for row in reader]
            avg_time = sum(times) / len(times)  # Calculer le temps moyen
            data[algorithm].append((size, avg_time))

    # Trie des données par taille
    for algorithm in data:
        data[algorithm].sort(key=lambda x: x[0])

    # Tracé des courbes
    plt.figure(figsize=(10, 6))
    for algorithm, values in data.items():
        sizes = [v[0] for v in values]
        times = [v[1] for v in values]
        plt.plot(sizes, times, marker='o', label=algorithm)

    plt.title("Temps d'exécution des algorithmes en fonction de la taille")
    plt.xlabel("Taille du graphe")
    plt.ylabel("Temps (secondes)")
    plt.legend()
    plt.grid(True)
    plt.show()

def display_repartition():
    # Récupérer les fichiers CSV dans le répertoire courant
    csv_files = [f for f in os.listdir('.') if f.startswith("results_") and f.endswith(".csv")]

    if not csv_files:
        print("Aucun fichier de résultats trouvé.")
        return

    colors = {"EK": "blue", "PR": "green", "min": "red"}  # Couleurs pour chaque algorithme

    for algorithm in ["EK", "PR", "min"]:
        # Filtrer les fichiers pour l'algorithme courant
        algo_files = [f for f in csv_files if f"results_{algorithm}_" in f]
        if not algo_files:
            continue

        plt.figure(figsize=(10, 6))
        for file in algo_files:
            parts = file.split('_')
            if len(parts) < 3:
                continue
            size = int(parts[2][4:-4])  # Extraire la taille depuis "sizeX.csv"

            with open(file, mode="r") as f:
                reader = csv.DictReader(f)
                times = [float(row["Temps (secondes)"]) for row in reader]
                plt.scatter([size] * len(times), times, alpha=0.6, color=colors.get(algorithm, "black"))

        # Configurer le graphe pour l'algorithme courant
        plt.title(f"Répartition des temps d'exécution pour l'algorithme {algorithm}")
        plt.xlabel("Taille du graphe")
        plt.ylabel("Temps (secondes)")
        plt.grid(True)
        plt.show()


def compare_EKPR_generate_data (n, size):
    test_bench = create_test_bench(n, size)  # Générer un banc de test commun pour les deux algorithmes
    results = []

    for i, graph in enumerate(test_bench):
        print(f"Test {i + 1}:")

        # Mesurer le temps pour Edmonds-Karp
        start_time_ek = perf_counter()
        maximize_EK(graph, display=False)
        end_time_ek = perf_counter()
        time_ek = end_time_ek - start_time_ek

        # Mesurer le temps pour Pousser-Réétiqueter
        start_time_pr = perf_counter()
        maximize_PR(graph, display=False)
        end_time_pr = perf_counter()
        time_pr = end_time_pr - start_time_pr

        print(f"Temps Edmonds-Karp : {time_ek:.6f} secondes")
        print(f"Temps Pousser-Réétiqueter : {time_pr:.6f} secondes")

        results.append([i + 1, time_ek, time_pr])

    # Sauvegarder les résultats dans un fichier CSV
    filename = f"compare_EKPR_size{size}.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Test", "Temps Edmonds-Karp (secondes)", "Temps Pousser-Réétiqueter (secondes)"])
        writer.writerows(results)

    print(f"Résultats sauvegardés dans le fichier {filename}")


def display_compare_EKPR():
    csv_files = [f for f in os.listdir('.') if f.startswith("compare_EKPR_") and f.endswith(".csv")]

    if not csv_files:
        print("Aucun fichier de comparaison trouvé.")
        return

    data = {}

    for file in csv_files:
        with open(file, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ek_time = float(row["Temps Edmonds-Karp (secondes)"])
                pr_time = float(row["Temps Pousser-Réétiqueter (secondes)"])
                if pr_time > 0:  # Éviter la division par zéro
                    ratio = ek_time / pr_time
                    size = int(file.split("size")[1].split(".csv")[0])
                    if size not in data:
                        data[size] = []
                    data[size].append(ratio)

    sizes = sorted(data.keys())
    worst_cases = [max(data[size]) for size in sizes]

    plt.plot(sizes, worst_cases, marker='o', label="Rapport pire EK/PR")

    plt.title("Rapport temps (EK/PR) dans le pire des cas")
    plt.xlabel("Taille du graphe")
    plt.ylabel("Rapport pire EK/PR")
    plt.legend()
    plt.grid(True)
    plt.show()

display_compare_EKPR()


