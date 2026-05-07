import numpy as np
from predire import ls
from entrainer import Entrainer
from time import perf_counter

class Cluster():
    def __init__(self, k:int, n:int, cerveau:Entrainer):
        self.k=k
        self.n=n
        self.cerveau = cerveau

    def partitionne(self) -> None:
        self.initialiser_matrice()
        self.positionner_centroides()
        historique_migrations = self.remplir_matrice_comparaison()

        #Tentative pour gérer la création du graphe.
        return self.formatter_resultat(), historique_migrations

    def initialiser_matrice(self) -> None:
        self.matrice_comparaison = np.full(self.cerveau.matrice.shape[0], -1)

    def positionner_centroides(self) -> None:
        indices = np.random.choice(self.cerveau.matrice.shape[0], size=self.k, replace=False)
        self.matrice_centroide = self.cerveau.matrice[indices]

    def remplir_matrice_comparaison(self):
        historique = []
        self.nb_iter = 0
        nb_migration = 0
        first_iter = True
        while nb_migration > 0 or first_iter:
            first_iter = False
            t = perf_counter()
            self.old_matrice_comparaison = self.matrice_comparaison.copy()

            nb_migration = np.sum(self.matrice_comparaison != self.old_matrice_comparaison)
            historique.append(int(nb_migration))

            for i in range(len(self.cerveau.matrice)):
                distances = [ls(self.cerveau.matrice[i],c) for c in self.matrice_centroide]
                index_cluster = distances.index(min(distances))
                self.matrice_comparaison[i] = index_cluster

            nb_migration = np.sum(self.matrice_comparaison != self.old_matrice_comparaison)

            self.nb_iter += 1
            self.print_iter(t, nb_migration)
            self.update_centroide()

        return historique
        
    def update_centroide(self):
        new_centroids = np.zeros_like(self.matrice_centroide)

        for k in range(self.k):
            mask = (self.matrice_comparaison == k)
            if np.any(mask):
                new_centroids[k] = self.cerveau.matrice[mask].mean(axis=0)

        self.matrice_centroide = new_centroids

    def print_iter(self, t:float, nb_migration:int):
        print(f'\nItération {self.nb_iter} : {perf_counter() - t:.2f} secondes.')
        print(f'{nb_migration} migrations')
        for i in range(self.k):
            print(f'Partition {i} : {(self.matrice_comparaison == i).sum()} mots.')
        print(f'\n*************************')
                

    def formatter_resultat(self) -> list[tuple[str, np.float64]]:
        list_resultat = []
        for i in range(self.k):
            list_partition = []
            for mot, values in self.cerveau.vocabulaire.items():
                list_partition.append((mot, round(float(ls(self.cerveau.matrice[values], self.matrice_centroide[i])),2)))
            list_partition = sorted(list_partition, key=lambda t:t[1])[:self.n]
            list_resultat.append(list_partition.copy())
        return list_resultat
            
