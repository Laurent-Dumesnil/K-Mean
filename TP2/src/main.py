from sys import argv
from time import perf_counter
from traceback import print_exc
from entrainerBD import EntrainerBD
from predire import Predire
from parser import Parser

PRINT_TIME = 1
PRINT_ALL = 2

QUITTER = 'q'

INVITE = f"""
Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul,
i.e. produit scalaire: 0, least-squares: 1, city-block: 2

Tapez {QUITTER} pour quitter.

"""

def demande_utilisateur(cerveau: EntrainerBD, verbose: int) -> None:
    reponse = input(INVITE)
    while reponse != QUITTER:
        try:
            mot, nb, methode = reponse.split()
            nb, methode = int(nb), int(methode)
            print()
            t = perf_counter()
            resultats = Predire.prediction(cerveau, mot, nb, methode)
            duree = perf_counter() - t
            for mot, score in resultats:
                print(f'{mot} --> {score}')
            if verbose >= PRINT_TIME:
                print(f'\nPrédiction effectuée en {duree: .2f} secondes.')

        except Exception as e:
            print(e)
        reponse = input(INVITE)

def main() -> int:
    
    try:
        taille_fenetre = int(argv[1])
        encodage, chemin = argv[2:4]
        if len(argv) > 4:
            verbose = int(argv[4])
        else:
            verbose = 0

        cerveau = EntrainerBD(taille_fenetre)
        t = perf_counter()
        cerveau.entraine(chemin, encodage)
        if verbose >= PRINT_TIME:
            print(f'Entraînement effectué en {perf_counter() - t:.2f} secondes.')
            if verbose >= PRINT_ALL:
                print(cerveau)
        demande_utilisateur(cerveau, verbose)

    except ValueError as ve:
        print(ve)
        return -2
    except Exception as e:
        # print_exc()
        print(e)
        return -1

    return 0

if __name__ == '__main__':
    quit(main())
