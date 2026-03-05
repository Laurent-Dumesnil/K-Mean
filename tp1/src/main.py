from sys import argv
from training import Training
from prediction import Prediction
from colorama import init, Fore, Style

def main():
    # window = argv[1]
    # file = argv[2]
    # encode =  argv[3]
    window = 10
    file = "C:/travail/GerminalUTF8.txt"
    encode = "UTF-8"

    init(autoreset=True)
    
    train = Training(window, file, encode)
    prediction = Prediction(train)
    exit = False
    while not exit:
        answers = input("\nEntrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, i.e. produit scalaire: 1, least-squares: 2, city-block:3\nTapez q pour quitter\n\n").strip().lower().split(" ")
        if answers[0] == "q":
            print(f"\n{Fore.RED}AU REVOIR\n")
            return 0
        elif len(answers) != 3:
            print('\nVous devez écrire selon ce pattern: "mot_recherché" "nombre entier" "nombre[1 à 3]"')
        else:
            try:
                prediction.word = answers[0]
                try:
                    synonym_count = int(answers[1])
                    method = int(answers[2])
                    result = prediction.predict(synonym_count, method)
                    print()

                    for key, value in result.items():
                        print(f'{Fore.LIGHTBLUE_EX}{key}{Style.RESET_ALL} --> {Fore.GREEN}{value}')
                except ValueError:
                    print('\nVous devez entrez un nombre entier comme deuxième et troisième paramètres')
            except ValueError as e:
                print(e)
    
if __name__ == '__main__':
    quit(main())