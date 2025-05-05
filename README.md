# SM602 : Résolution de Problèmes de Flots

## Description
Projet du module de recherche opérationnelle SM602 vu à l'Efrei.
Ce projet implémente plusieurs algorithmes pour résoudre des problèmes de flots dans les réseaux, notamment :
- Algorithme d'Edmonds-Karp pour la maximisation de flot
- Algorithme de Push-Relabel pour la maximisation de flot 
- Algorithme de minimisation des coûts

## Prérequis
- Python 3.x

## Structure du projet
- `main.py` : Point d'entrée du programme avec interface utilisateur
- `maxEK.py` : Implémentation de l'algorithme d'Edmonds-Karp
- `maxPR.py` : Implémentation de l'algorithme Push-Relabel
- `minC.py` : Implémentation de l'algorithme de minimisation des coûts
- `graph.py` : Fonctions de manipulation des graphes
- `display.py` : Fonctions d'affichage des matrices et résultats
- `complexity.py` : Fonctions permettant de tester la complexité des matrices

## Format des fichiers d'entrée
Les graphes doivent être fournis dans des fichiers `.txt` avec le format suivant :
```txt
n                    # Nombre de sommets
matrice_capacites    # Matrice n×n des capacités
[matrice_couts]      # Matrice n×n des coûts (optionnelle)
