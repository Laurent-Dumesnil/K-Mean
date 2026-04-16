from sys import argv
from re import findall
import numpy as np
import numpy.typing as npt

class Entrainer():
    def __init__(self, taille_fenetre: int) -> None:
        self.taille_fenetre = taille_fenetre

    def __str__(self) -> str:
        return f'\n{self._vocabulaire}\n\n{self._matrice}\n'

    @property
    def matrice(self) -> npt.NDArray[np.float64]:
        return self._matrice

    @property
    def vocabulaire(self) -> dict:
        return self._vocabulaire

    def entraine(self, chemin: str, encodage: str) -> None:
        self.parse_texte(chemin, encodage)
        self.init_vocabulaire()
        self.indexer_vocabulaire()
        self.init_cooccurrences()
        self.compter_cooccurrences()

    def parse_texte(self, chemin: str, encodage: str) -> None:
        with open(chemin, encoding = encodage) as f:
            self._texte = findall(r'\w+', f.read().lower())
        
    def init_vocabulaire(self) -> None:
        self._vocabulaire =  {}
    
    def indexer_vocabulaire(self) -> None:
        for mot in self._texte:
            if mot not in self._vocabulaire:
                self._vocabulaire[mot] = len(self._vocabulaire)

    def init_cooccurrences(self) -> None:
        self._matrice = np.zeros( ( len(self._vocabulaire), len(self._vocabulaire) ) )

    def compter_cooccurrences(self) -> None:
        for i in range(len(self._texte)):
            for j in range(1, self.taille_fenetre//2 + 1):
                if i - j >= 0:
                    self._matrice[self._vocabulaire[self._texte[i]], self._vocabulaire[self._texte[i - j]]] += 1
                if i + j < len(self._texte):
                    self._matrice[self._vocabulaire[self._texte[i]], self._vocabulaire[self._texte[i + j]]] += 1

def main() -> int:
    taille_fenetre = int(argv[1])
    encodage, chemin = argv[2:4]

    test = np.array([[0, 3, 2, 0, 1], [3, 2, 4, 8, 4], [2, 4, 0, 2, 0], [0, 8, 2, 2, 3], [1, 4, 0, 3, 0]], dtype=np.float64)
    cerveau = Entrainer(taille_fenetre)
    cerveau.entraine(chemin, encodage)
    if np.sum(test != cerveau.matrice):
        print('Erreur!')
        return 1
    
    print('OK!')
    return 0

if __name__ == '__main__':
    quit(main())

