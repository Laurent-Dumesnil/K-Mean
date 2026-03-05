from sys import argv
import re
import numpy as np

class Training():
        def __init__(self, window, file, encode):
                
                self.__text = self.__read_text(file, encode)
                self.__words = re.findall(r"\b\w+\b", self.__text.lower())
                self.window = window
                self.__word_dict = self.__create_dict()
                self.__coocurence_matrix = self.__create_matrix()
                self.__fill_coocurence_matrix()
                self.__lookup_table = self.__create_lookup_table()

        def __create_lookup_table(self):
                lookup = []
                for keys, _ in self.__word_dict.items():
                        lookup.append(keys)
                return lookup

        def __read_text(self, file, encode):
                try:
                        f = open(file, encoding=encode)
                        text = f.read()
                        f.close()
                except Exception:
                        print(f"\nErreur lors de l'ouverture du fichier. Vérifiez que votre chemin: {file} et votre encodage: {encode} sont valides\n")
                        quit()

                return text
        
        def __create_dict(self):
                dictionnary =  dict.fromkeys(self.__words)
                index = 0

                for index, key in enumerate(dictionnary):
                        dictionnary[key] = index
                return dictionnary

        def __create_matrix(self):
                size = len(self.__word_dict)
                return np.array(np.zeros((size, size)))
                

        def __fill_coocurence_matrix(self):
                neighbors_qty = self.__window//2
                n = len(self.__words)

                #on parcours chaque mot du texte
                for i in range(n):
                        #On trouve l'index de ce mot dans le __word_dict
                        index = self.__word_dict[self.__words[i]]
                        #On trouve les voisins avant
                        for offset in range(-neighbors_qty, neighbors_qty+1):
                                #Empecher le outofbound
                                if offset == 0:
                                        continue

                                j = i + offset

                        #On trouve les voisins après
                                if 0 <= j < n:
                                        neighbor = self.__words[j]
                                        idx = self.__word_dict[neighbor]
                                        self.__coocurence_matrix[index, idx] += 1
        
        @property
        def word_dict(self):
                return self.__word_dict
        
        @property
        def coocurence_matrix(self):
                return self.__coocurence_matrix
        
        @property
        def lookup_table(self):
                return self.__lookup_table
        
        @property
        def window(self):
                return self.__window
        
        @window.setter
        def window(self, value):
                try:
                        if value <= 2 and value > 21:
                                print("Votre fenêtre doit être comprise entre 3 et 21")
                                quit()
                        self.__window = int(value)

                except Exception:
                        raise TypeError('\nLa fenêtre doit être un entier')
                





        
