from sys import argv
from time import perf_counter
from traceback import print_exc
from entrainerBD import EntrainerBD
from predire import Predire
from parser import Parser
from DAO import DatabaseService
from cluster import Cluster
from graphe import Graphe
import os

#Commandes pour faire des tests pour Laurent
    # main.py -b
    # main.py -e -t5 --encodage UTF-8 --chemin ..\doc\GerminalUTF8.txt
    # main.py -e -t5 --encodage UTF-8 --chemin ..\doc\LeVentreDeParisUTF8.txt
    # main.py -e -t5 --encodage UTF-8 --chemin ..\doc\LesTroisMousquetairesUTF8.txt
    # main.py -e -t5 --encodage UTF-8 --chemin ..\doc\DonQuichotteUTF8.txt
    # main.py -c -t5 -k5 -n10 


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

def afficher_cluster(results:list[tuple[str, float]]):
    for i in range(len(results)):
        print(f'\nPartition {i}:')
        for word, score in results[i]:
            print(f'        {word} -> {score}')

def main() -> int:
    p = Parser()
    args = p.parse()

    s = DatabaseService()
    
    
    try:
        cerveau = EntrainerBD(args.t, s)
        t = perf_counter()
        
        if args.e:
            cerveau.entraine(args.chemin, args.encodage)
        
        if args.b:
            s.create_table()

        if args.p:
            cerveau.charger_bd()
            demande_utilisateur(cerveau, args.v)

        if args.c:
            cerveau.charger_bd()
            c  = Cluster(args.k, args.n, cerveau)
            clusters, historique = c.partitionne()
            
            afficher_cluster(clusters)
            if args.graphe:
                graphe = Graphe(historique)
                graphe.afficher_migrations()
            #afficher_cluster(c.partitionne())

        if args.v >= PRINT_TIME:
            print(f'Opération effectuée en {perf_counter() - t:.2f} secondes.')
        
        if args.v >= PRINT_ALL:
            if hasattr(cerveau,'_vocabulaire') and cerveau._vocabulaire:
                print(cerveau)
            else:
                print('La base de donnée est vide.')

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
    