from sys import argv
import re
import numpy as np

class Training():
        def __init__(self, window, file, encode):
                try:
                        self.text = self.read_text(file, encode)
                        self.words = re.findall(r"\b\w+\b", self.text.lower())
                        self.window = int(window)
                except Exception:
                        print(f"\nErreur lors de l'ouverture du fichier. Vérifiez que votre fenêtre: {window}, que votre chemin: {file} et votre encodage: {encode} sont valides\n")
                        quit()

                self.__word_dict = self.__create_dict(self.words)
                self.__coocurence_matrix = self.__create_matrix(self.__word_dict)
                self.__fill_coocurence_matrix(self.coocurence_matrix, self.words, self.__word_dict, self.window)
                self.__lookup_table = self.__create_lookup_table()

        def __create_lookup_table(self):
                lookup = []
                for keys, _ in self.__word_dict.items():
                        lookup.append(keys)
                return lookup

        def read_text(self, file, encode):
                f = open(file, encoding=encode)
                text = f.read()
                f.close()

                return text
        
        def __create_dict(self, words):
                dictionnary =  dict.fromkeys(words)
                index = 0

                for index, key in enumerate(dictionnary):
                        dictionnary[key] = index
                return dictionnary

        def __create_matrix(self, __word_dict):
                size = len(__word_dict)
                return np.array(np.zeros((size, size)))
                

        def __fill_coocurence_matrix(self, matrix, words, __word_dict, window):
                neighbors_qty = window//2
                n = len(words)

                #on parcours chaque mot du texte
                for i in range(n):
                        #On trouve l'index de ce mot dans le __word_dict
                        index = __word_dict[words[i]]
                        #On trouve les voisins avant
                        for offset in range(-neighbors_qty, neighbors_qty+1):
                                #Empecher le outofbound
                                if offset == 0:
                                        continue

                                j = i + offset

                        #On trouve les voisins après
                                if 0 <= j < n:
                                        neighbor = words[j]
                                        idx = __word_dict[neighbor]
                                        matrix[index, idx] += 1
                return matrix
        
        @property
        def word_dict(self):
                return self.__word_dict
        
        @property
        def coocurence_matrix(self):
                return self.__coocurence_matrix
        
        @property
        def lookup_table(self):
                return self.__lookup_table





        
