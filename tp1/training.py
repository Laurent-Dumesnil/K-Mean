from sys import argv
import re

def lire_fichier(chemin, encodage):
        f = open(chemin, encoding=encodage)
        texte = f.read()
        f.close()

        return texte
