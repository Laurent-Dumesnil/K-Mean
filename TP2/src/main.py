from sys import argv
from time import perf_counter
from traceback import print_exc
from entrainerBD import EntrainerBD
from predire import Predire
from parser import Parser
import os

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
    p = Parser()
    args = p.parse()
    
    try:
        cerveau = EntrainerBD(args.t)
        if args.e:
            t = perf_counter()
            cerveau.entraine(args.chemin, args.encodage)
        
        if args.b:
            if os.path.exists('ai2.db'):  
                cerveau.db.delete_from()

        if args.v >= PRINT_TIME:
            print(f'Entraînement effectué en {perf_counter() - t:.2f} secondes.')
        if args.v >= PRINT_ALL:
            print(cerveau)

        if args.p:
            demande_utilisateur(cerveau)

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