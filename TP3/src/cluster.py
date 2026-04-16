import numpy as np
from entrainerBD import EntrainerBD
from DAO import DatabaseService

class Cluster():
    def __init__(self, k:int, n:int, cerveau:EntrainerBD):
        self.k=k
        self.n=n
        self.cerveau = cerveau

    def partitionne(self) -> None:
        self.initialiser_matrice()
        self.positionner_centroides()
        self.remplir_matrice_comparaison()
        self.lancer_migration()

    def initialiser_matrice(self) -> None:
        self.matrice_comparaison = np.zeros(self.cerveau.matrice.shape)

    def positionner_centroides(self) -> None:
        copy = self.cerveau.matrice.copy()
        np.random.shuffle(copy)
        self.matrice_centroide = copy[:self.k]
        
    def remplir_matrice_comparaison(self) -> None:
        for val in self.cerveau.matrice:
            closest = 0
            for i, centroide in enumerate(self.matrice_centroide):
                if centroide-val < self.matrice_centroide[closest]:
                    closest = i
            self.matrice_comparaison.put(closest)
                

    def lancer_migration(self) -> dict[str:dict[str:float]]:
        pass


# if __name__ == '__main__':
#     cerveau = EntrainerBD(5, DatabaseService())
#     cerveau.charger_bd()
#     c = Cluster(3,5,cerveau)