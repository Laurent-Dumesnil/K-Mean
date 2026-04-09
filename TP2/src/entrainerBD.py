from entrainer import Entrainer
from DAO import DataManager
from typing import override, Self
import numpy as np

class EntrainerBD(Entrainer):
    def __init__(self:Self, taille_fenetre: int):
        super().__init__(taille_fenetre)
        self.db:DataManager = DataManager()

    @override
    def indexer_vocabulaire(self:Self) -> None:
        mots_db = self.db.get_words()
        for rangee in mots_db:
            self.vocabulaire[rangee[0]] = rangee[1] -1
        mots_a_ajouter = {}
        for mot in self._texte:
            if mot not in self._vocabulaire:
                self._vocabulaire[mot] = len(self.vocabulaire)
                mots_a_ajouter[mot] = len(self.vocabulaire)

        self.db.add_words(mots_a_ajouter)

    @override
    def init_cooccurrences(self:Self) -> None:
        super().init_cooccurrences()
        self.old_matrice = self._matrice.copy()
        coo_db = self.db.get_coocurence(self.taille_fenetre)
        for rangee in coo_db:
            self.old_matrice[rangee[0]][rangee[1]] = rangee[2]
        self._matrice = self.old_matrice.copy()

    @override
    def compter_cooccurrences(self:Self)-> None:
        super().compter_cooccurrences()
        self.ajouter_coo_bd()

    def ajouter_coo_bd(self:Self) -> None:
        coo_a_ajouter = self._matrice - self.old_matrice
        indices = np.argwhere(coo_a_ajouter != 0)
        inverse = np.sort(indices, axis=1)
        index_sans_doublons = np.unique(inverse, axis=0)
        list_a_ajouter = []
        for i in range(np.size(index_sans_doublons, axis = 0)):
            list_a_ajouter.append([int(index_sans_doublons[i][0]),int(index_sans_doublons[i][1]), self.taille_fenetre, int(self.matrice[index_sans_doublons[i][0]][index_sans_doublons[i][1]])])

        self.db.add_coocurence(list_a_ajouter)

