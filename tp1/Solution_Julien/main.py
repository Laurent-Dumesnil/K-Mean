from sys import argv
from training import Training

def main():
    # window = argv[1]
    # file = argv[2]
    # encode =  argv[3]

    window = 5
    file = "C:/travail/AmisTest.txt"
    encode = "UTF-8"
    
    train = Training(window, file, encode)
    print(train.matrix)
    
if __name__ == '__main__':
    quit(main())