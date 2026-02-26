from sys import argv
from training import Training
from prediction import Prediction
from colorama import init, Fore, Style, Back

def main():
    window = argv[1]
    file = argv[2]
    encode =  argv[3]

    init(autoreset=True)
    
    train = Training(window, file, encode)
    exit = False
    while not exit:
        answers = input("\nEntrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, i.e. produit scalaire: 1, least-squares: 2, city-block:3\nTapez q pour quitter\n\n").strip().lower().split(" ")
        if answers[0] == "q":
            print(f"\n{Fore.RED}AU REVOIR\n")
            return 0
        elif len(answers) != 3:
            print('\nVous devez écrire selon ce pattern: "mot_recherché" "nombre_entier" "nombre_0_1_2"')
        else:
            try:
                prediction = Prediction(train, answers[0], answers[1], answers[2])
                print()

                for key, value in prediction.result.items():
                    print(f'{Fore.LIGHTBLUE_EX}{key}{Style.RESET_ALL} --> {Fore.GREEN}{value}')
            except ValueError as e:
                print(e)
    
if __name__ == '__main__':
    quit(main())