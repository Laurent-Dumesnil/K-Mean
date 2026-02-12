from sys import argv
import training as tr
import research as rs
import re


def main():
    chemin = argv[1]
    encodage =  argv[2]
    txt = tr.lire_fichier(chemin, encodage)
    print(txt)

if __name__ == '__main__':
    quit(main())