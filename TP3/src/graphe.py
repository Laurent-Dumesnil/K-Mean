import matplotlib.pyplot as plt
import numpy as np

class Graphe():
    def __init__(self, historique:list[int]):
        self.historique = historique

    
    def afficher_migrations(self)->None:
        if not self.historique:
            raise ValueError(f"Il n'est pas possible de faire l'affichage du graphique puisque nous n'avons pas pu charger l'historique de migration.")
        
        iter = range(1, len(self.historique) + 1)

        plt.plot(iter, self.historique, marker='o', linestyle='-', color='teal', label='Migrations')
        plt.title("Convergence de l'algorithme de partitionnement")
        plt.xlabel("Nombre d'itérations")
        plt.ylabel("Nombre de migrations")
        plt.grid(True)
        plt.legend()
        plt.show()