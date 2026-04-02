from entrainer import Entrainer
from DAO import DataManager
import numpy as np

class EntrainerBD(Entrainer):
    def __init__(self, taille_fenetre: int):
        super().__init__(taille_fenetre)
        self.db = DataManager()

    def indexer_vocabulaire(self) -> None:
        mots_db = self.db.get_words()
        for rangee in mots_db:
            self.vocabulaire[rangee[0]] = rangee[1] -1
        mots_a_ajouter = {}
        for mot in self._texte:
            if mot not in self._vocabulaire:
                self._vocabulaire[mot] = len(self.vocabulaire)
                mots_a_ajouter[mot] = len(self.vocabulaire)
        self.db.add_words(mots_a_ajouter)
        print(mots_a_ajouter)

    def init_cooccurrences(self) -> None:
        super().init_cooccurrences()
        # self.curseur.execute("SELECT * FROM coo")
        # for rangee in self.curseur.fetchall():
        #     self._matrice[self.vocabulaire[rangee[0]], self.vocabulaire[rangee[1]]] = rangee[2]
        #     self._matrice[self.vocabulaire[rangee[1]], self.vocabulaire[rangee[0]]] = rangee[2]
        # print(self._matrice)

    def update_mots(self) -> None:
        self.db.add_words(self.vocabulaire)


if __name__ == '__main__': #À supprimer, pour test en attendant
    quit(EntrainerBD(7).entraine("C:/travail/C62_ProulxJeremie_DumesnilLaurent_LamontagneJulien/TP2/doc/AmisTest.txt", "UTF-8"))
