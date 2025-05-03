from operator import truth

from display import display_graph, display_flow
from graph import *
from maxEK import *
from maxPR import *
from minC import *

def menu():
    import os
    while True:
        # Lister tous les fichiers .txt dans le répertoire courant
        txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
        if not txt_files:
            print("Aucun fichier .txt trouvé dans le répertoire courant.\n")
            return

        print("Fichiers disponibles :\n")
        for i, file in enumerate(txt_files, start=1):
            print(f"    {i}. {file}")
        print()
        try:
            choice = int(input("Choisissez un fichier (entrez le numéro) : "))
            if choice < 1 or choice > len(txt_files):
                print("Choix invalide.\n")
                continue
            selected_file = txt_files[choice - 1]
        except ValueError:
            print("Entrée invalide.\n")
            continue

        # Lire le graphe depuis le fichier sélectionné
        graph = read_graph(selected_file)
        display_graph(graph)
        if not graph:
            print("\nErreur lors de la lecture du fichier.")
            continue

        C, F, cost = graph

        # Vérifier s'il s'agit d'un problème de maximisation ou de minimisation
        if cost == []:  # Problème de maximisation
            print("\nChoisissez l'algorithme à utiliser :")
            print("1. Edmonds-Karp")
            print("2. Pousser-réétiqueter")

            try:
                algo_choice = int(input("\nEntrez votre choix (1 ou 2) : "))
                if algo_choice == 1:
                    print("Résolution avec l'algorithme de Ford-Fulkerson (Edmonds-Karp):")
                    maximize_EK(graph, display=True)
                elif algo_choice == 2:
                    print("Résolution avec l'algorithme de relabel-to-push :")
                    maximize_PR(graph, display=True)
                else:
                    print("\nChoix invalide.")
                    continue
            except ValueError:
                print("\nEntrée invalide.")
                continue
        else:  # Problème de minimisation
            try:
                n = int(input("Entrez la valeur du flot à utiliser : "))
                print("\nRésolution avec l'algorithme de minimisation des coûts...")
                minimize_C(graph, n, display=True)
            except ValueError:
                print("\nEntrée invalide.")
                continue

        # Proposer de recommencer
        retry = input("\nVoulez-vous recommencer ? (o/n) : ").strip().lower()
        if retry != 'o':
            print("Fin du programme.")
            break




if __name__ == "__main__":
    print("Projet de recherche opérationnelle : Résolution de problèmes de flots\n")
    menu()


