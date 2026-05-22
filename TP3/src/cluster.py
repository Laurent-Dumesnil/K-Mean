import numpy as np
from predire import ls
from entrainer import Entrainer
from time import perf_counter

class Cluster():
    def __init__(self, k:int, n:int, cerveau:Entrainer):
        self.k=k
        self.n=n
        self.cerveau = cerveau

        self.matrice = self.cerveau.matrice 

    def partitionne(self) -> None:
        self.initialiser_matrice()
        self.positionner_centroides()
        historique_migrations = self.remplir_matrice_comparaison()

        return self.formatter_resultat(), historique_migrations

    def initialiser_matrice(self) -> None:
        self.matrice_comparaison = np.full(self.matrice.shape[0], -1)

    def positionner_centroides(self) -> None:
        indices = np.random.choice(self.matrice.shape[0], size=self.k, replace=False)
        self.matrice_centroide = self.matrice[indices]

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

            for i in range(len(self.matrice)):
                distances = [ls(self.matrice[i],c) for c in self.matrice_centroide]
                index_cluster = distances.index(min(distances))
                self.matrice_comparaison[i] = index_cluster

            nb_migration = np.sum(self.matrice_comparaison != self.old_matrice_comparaison)

            historique.append(int(nb_migration))
            
            self.nb_iter += 1
            self.print_iter(t, nb_migration)
            self.update_centroide()

        return historique
        
    def update_centroide(self):
        new_centroids = np.zeros_like(self.matrice_centroide)

        for k in range(self.k):
            mask = (self.matrice_comparaison == k)
            if np.any(mask):
                new_centroids[k] = self.matrice[mask].mean(axis=0)

        self.matrice_centroide = new_centroids

    def print_iter(self, t:float, nb_migration:int):
        print(f'\nItération {self.nb_iter} : {perf_counter() - t:.2f} secondes.')
        print(f'{nb_migration} migrations')
        for i in range(self.k):
            print(f'Partition {i} : {(self.matrice_comparaison == i).sum()} mots.')
        print(f'\n*************************')            
        
    def formatter_resultat(self) -> list[tuple[str, np.float64]]:
        list_resultat = [[] for _ in range(self.k)]
    
        for mot, values in self.cerveau.vocabulaire.items():
            centroid = self.matrice_comparaison[values]
            list_resultat[centroid].append((mot, round(float(ls(self.matrice[values], self.matrice_centroide[centroid])),2)))
            
        for i, result in enumerate(list_resultat):
            list_resultat[i] = sorted(result, key=lambda t:t[1])[:self.n]
            
        return list_resultat
    
            
