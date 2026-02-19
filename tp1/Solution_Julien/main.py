from sys import argv
from training import Training
from prediction import Prediction

def main():
    # window = argv[1]
    # file = argv[2]
    # encode =  argv[3]

    window = 5
    file = "C:/travail/AmisTest.txt"
    encode = "UTF-8"
    
    train = Training(window, file, encode)
    print(train.matrix)
    exit = False
    while not exit:
        answers = input("Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, i.e. produit scalaire: 0, least-squares: 1, city-block:2\nTapez q pour quitter\n\n").strip().lower().split(" ")
        if answers[0] == "q":
            print("AU REVOIR")
            return 0
        elif len(answers) != 3:
            raise ValueError('Vous devez écrire selon ce pattern: "mot_recherché" "nombre_entier" "nombre_0_1-2"')
        prediction = Prediction(train, answers[0], answers[1], answers[2])

        for key, value in prediction.result.items():
            print(f'{key} --> {value}')
    
if __name__ == '__main__':
    quit(main())