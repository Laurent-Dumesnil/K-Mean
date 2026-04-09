import numpy as np
import numpy.typing as npt
from entrainer import Entrainer

STOP = set('l le la les au aux un une du des c ça ce cette cet ces celle celui celles ceux je j tu il elle on nous vous ils elles me m te t se s y à de pour sans par mais ou et donc car ni or ne n pas dans que qui qu de d mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs lui en quel quelle quelles lequel laquelle lesquels lesquelles dont quoi quand où comment pourquoi sur dessus tout tous toutes avec comme avec'.split())

def ls(u: npt.NDArray[np.float64], v: npt.NDArray[np.float64]) -> np.float64:
    return np.sum((u-v)**2)

def cb(u: npt.NDArray[np.float64], v: npt.NDArray[np.float64]) -> np.float64:
    return np.sum(np.abs(u-v))

class Predire():

    fonctions = [np.dot, ls, cb]

    @staticmethod
    def prediction(cerveau: Entrainer, mot_recherche: str, nb: int, methode: int) -> list[tuple[str, np.float64]]:
        print(cerveau.vocabulaire)
        
        if mot_recherche not in cerveau.vocabulaire:
            raise Exception(f'"{mot_recherche}" n\'est pas dans le vocabulaire.')
        
        index_recherche = cerveau.vocabulaire[mot_recherche]
        v = cerveau.matrice[index_recherche]
        fonction = Predire.fonctions[methode]
        resultats = []
        for mot, index in cerveau.vocabulaire.items():
            if index != index_recherche and mot not in STOP:
                resultats.append( (mot, fonction(v, cerveau.matrice[index])) )
        return sorted(resultats, key=lambda t:t[1], reverse = fonction == np.dot)[:nb]

        
        
