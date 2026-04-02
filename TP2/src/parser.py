import argparse

class Parser():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Parser to read user input')

    def build_parser(self):

        group_modes = self.parser.add_mutually_exclusive_group('Modes entrainement, prediction, base de donnees', required=True)
        group_modes.add_argument('-e', action='store_true', help='Entrainer le modèle')
        group_modes.add_argument('-p', action='store_true', help='Prédire les synonymes')
        group_modes.add_argument('-b', action='store_true', help='Regénérer la BD')


        group_entrainement  = self.parser.add_argument_group('Entrainement')
        group_entrainement.add_argument('-t', type=int, help='Sélection de la taille de la fenêtre')
        group_entrainement.add_argument('--encodage', help="Sélection du type d'encodage du texte")
        group_entrainement.add_argument('--chemin', help='Sélection du chemin pour accéder au texte à analyser')

    def parse(self):
        args = self.parser.parse_args()
        self._validate(args)
        return args
    
    def _validate(args, parser):
        if args.e:
            missing = []
            if args.t is None:
                missing.append("-t")
            if args.encodage is None:
                missing.append("--encodage")
            if args.chemin is None:
                missing.append("--chemin")
            
            if missing:
                parser.error(f"L'option -e requiert aussi : {', '.join(missing)}")

        elif args.p:
            missing = []
            if args.t is None:
                missing.append("-t")

            if missing:
                    parser.error(f"L'option -p requiert aussi : -t")
