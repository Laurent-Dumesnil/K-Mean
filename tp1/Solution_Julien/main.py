from sys import argv
from training import Training

def main():
    window = argv[1]
    file = argv[2]
    encode =  argv[3]
    try:
        txt = Training.read_text(file, encode)
    except Exception:
        print("Erreur lors de l'ouverture")

    dict = Training.extract_words(txt)

    matrix = Training.fill_matrix_vector(txt, dict, window)
    print(matrix)
    
if __name__ == '__main__':
    quit(main())