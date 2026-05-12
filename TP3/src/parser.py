import argparse
import os

class Parser():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Parser to read user input')
        self.build_parser()

    def build_parser(self):

        group_modes = self.parser.add_mutually_exclusive_group(required=True)
        group_modes.add_argument('-e', action='store_true', help='Entrainer le modèle')
        group_modes.add_argument('-p', action='store_true', help='Prédire les synonymes')
        group_modes.add_argument('-b', action='store_true', help='Regénérer la BD')
        group_modes.add_argument('-c', action='store_true', help='Génère des clusters de mots')

        group_entrainement  = self.parser.add_argument_group('Entrainement')
        group_entrainement.add_argument('-t', type=int, help='Sélection de la taille de la fenêtre')
        group_entrainement.add_argument('--encodage', help="Sélection du type d'encodage du texte")
        group_entrainement.add_argument('--chemin', help='Sélection du chemin pour accéder au texte à analyser')

        self.parser.add_argument('-v', type=int, nargs='?', const=0, default=0, help='Niveau de verbosité (0, 1 ou 2)')
        self.parser.add_argument('--normaliser', action='store_true', help="Normalisation des données")
        self.parser.add_argument('--conserver', type=int, help="Permet de conserver les x nombre de colonnes (features) les plus représentées")

        group_cluster = self.parser.add_argument_group('Cluster')
        group_cluster.add_argument('-k', type=int, help='Sélection du nombre de cluster')
        group_cluster.add_argument('-n', type=int, help='Nombre de mots à afficher par cluster')
        group_cluster.add_argument('--graphe', action='store_true', help="Génère un graphique représentant le nombre de migrations en fonction du nombre d'itérations")
    
    
    def parse(self):
        args = self.parser.parse_args()
        self._validate(args)
        return args
    
    def _validate(self, args):

        requirements = {
            'e': ['t','encodage', 'chemin'],
            'p': ['t'],
            'b':[],
            'c':['t','k','n']
        }
        mode = next((mode for mode in requirements if getattr(args, mode)), None)
        if mode :
            if args.t is not None and args.t <= 0:
                self.parser.error('\nLa taille de la fenêtre doit être plus grand que 0.')
            
            if args.chemin:
                if not os.path.isfile(args.chemin):
                    self.parser.error("\nLe chemin n'est pas valide.")
                
                try:
                    _ = open(args.chemin, encoding=args.encodage)
                except:
                    self.parser.error("\nL'encodage sélectionné n'est pas valide.")

            if args.k is not None and args.k <= 1:
                self.parser.error('\nLe nombre de cluster doit au moins être égal à 2.')

            if args.n is not None and args.n <=0:
                self.parser.error('\nLe nombre de mot à afficher par cluster doit être plus grand que 0.')

            if args.conserver is not None and args.conserver < 0:
                self.parser.error('\nLe nombre de colonnes à conserver doit être plus grand que 0.')

            missing = [f'--{req}' if len(req) > 1 else f'-{req}'
                       for req in requirements[mode]
                       if getattr(args, req) is None
                       ]
            if missing:
                self.parser.error(f"\nL'option {mode} requiert aussi : {', '.join(missing)}.")