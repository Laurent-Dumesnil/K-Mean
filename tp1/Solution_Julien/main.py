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
        answers = input("Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, i.e. produit scalaire: 0, least-squares: 1, city-block:2\nTapez q pour quitter\n\n").split(" ")
        for answer in answers:
            if answer == "q":
                print("AU REVOIR")
                return
        pred = Prediction(train, answers)
    
if __name__ == '__main__':
    quit(main())