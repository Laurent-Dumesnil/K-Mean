import argparse

class Parser():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Parser to read user input')
        self.build_parser()

    def build_parser(self):

        group_modes = self.parser.add_mutually_exclusive_group(required=True)
        group_modes.add_argument('-e', action='store_true', help='Entrainer le modèle')
        group_modes.add_argument('-p', action='store_true', help='Prédire les synonymes')
        group_modes.add_argument('-b', action='store_true', help='Regénérer la BD')

        group_entrainement  = self.parser.add_argument_group('Entrainement')
        group_entrainement.add_argument('-t', type=int, help='Sélection de la taille de la fenêtre')
        group_entrainement.add_argument('--encodage', help="Sélection du type d'encodage du texte")
        group_entrainement.add_argument('--chemin', help='Sélection du chemin pour accéder au texte à analyser')

        self.parser.add_argument('-v', type=int, default=0, help='Niveau de verbosité')


#valider sur la taille de la fenetre > 0
#valide sur chemin et encodage

    def parse(self):
        args = self.parser.parse_args()
        self._validate(args)
        return args
    
    def _validate(self, args):

        requirements = {
            'e': ['t','encodage', 'chemin'],
            'p': ['t'],
            'b':[]
        }
        mode = next((mode for mode in requirements if getattr(args, mode)), None)
        if mode :
            if args.t is not None and args.t <= 0:
                self.parser.error('\nLa taille de la fenêtre doit être plus grand que 0')
            
            if args.chemin:
            
            if args.encodage
            missing = [f'--{req}' if len(req) > 1 else f'-{req}'
                       for req in requirements[mode]
                       if getattr(args, req) is None
                       ]
            if missing:
                self.parser.error(f"L'option {mode} requiert aussi : {', '.join(missing)}")