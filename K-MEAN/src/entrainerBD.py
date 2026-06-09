from entrainer import Entrainer
from DAO import DatabaseService
from typing import override, Self
import numpy as np

class EntrainerBD(Entrainer):
    def __init__(self:Self, taille_fenetre: int, db:DatabaseService):
        super().__init__(taille_fenetre)
        self.db = db

    @override
    def indexer_vocabulaire(self:Self) -> None:
        self.charger_mots()
        mots_a_ajouter = {}
        for mot in self._texte:
            if mot not in self.vocabulaire:
                self.vocabulaire[mot] = len(self.vocabulaire)
                mots_a_ajouter[mot] = self.vocabulaire[mot]

        self.db.add_words(mots_a_ajouter)

    @override
    def init_cooccurrences(self:Self) -> None:
        super().init_cooccurrences()
        self.charger_coocurences()

    @override
    def compter_cooccurrences(self:Self) -> None:
        super().compter_cooccurrences()
        self.ajouter_coo_bd()

    def charger_bd(self:Self, conserver:int, normaliser:bool = False) -> None:
        super().init_vocabulaire()
        self.charger_mots()
        super().init_cooccurrences()
        self.charger_coocurences()
        if conserver is not None and conserver > 0:
            conserve_matrix = self._matrice
            sommes = np.sum(self._matrice, axis=0)
            indexes = np.argsort(sommes)[::-1][:conserver]
            self._matrice = np.zeros((len(conserve_matrix), conserver))

            self._matrice[:] = conserve_matrix[:,indexes][:]

        if normaliser:
            normes = np.linalg.norm(self._matrice, axis=1, keepdims=True)
            self._matrice /= normes
        

    def charger_mots(self:Self) -> None:
        mots_db = self.db.get_words()
        for mot, idx in mots_db:
            self.vocabulaire[mot] = idx
    
    def charger_coocurences(self:Self) -> None:
        self.old_matrice = self._matrice.copy()
        coo_db = self.db.get_coocurence(self.taille_fenetre)
        for row,col,val in coo_db:
            self.old_matrice[row][col] = val
            self.old_matrice[col][row] = val
        self._matrice = self.old_matrice.copy()



    def ajouter_coo_bd(self:Self) -> None:
        coo_a_ajouter = self._matrice - self.old_matrice
        indices = np.argwhere(coo_a_ajouter != 0)
        inverse = np.sort(indices, axis=1)
        index_sans_doublons = np.unique(inverse, axis=0)
        list_a_ajouter = []
        for i in index_sans_doublons:
            list_a_ajouter.append([int(i[0]), int(i[1]), self.taille_fenetre, int(self.matrice[i[0]][i[1]])])

        self.db.add_coocurence(list_a_ajouter)

if __name__ == "__main__":
    EntrainerBD(7, DatabaseService()).entraine("C:/travail/C62_ProulxJeremie_DumesnilLaurent_LamontagneJulien/TP2/doc/AmisTest.txt","UTF-8")