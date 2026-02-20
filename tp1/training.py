from sys import argv
import re
import numpy as np

class Training():
        def __init__(self, window, file, encode):
                try:
                        self.text = self.read_text(file, encode)
                        self.words = re.findall(r"\b\w+\b", self.text.lower())
                except Exception:
                        print("Erreur lors de l'ouverture du fichier")

                self.dict = self.create_dict(self.words)
                self.matrix = self._create_matrix(self.dict)
                self.fill_matrix_vector(self.matrix, self.words, self.dict, window)
                self.lookup_table = self.create_lookup_table()

        def create_lookup_table(self):
                lookup = []
                for keys, _ in self.dict.items():
                        lookup.append(keys)
                return lookup

        def read_text(self, file, encode):
                f = open(file, encoding=encode)
                text = f.read()
                f.close()

                return text
        
        def create_dict(self, words):
                d =  dict.fromkeys(words)
                index = 0

                for index, key in enumerate(d):
                        d[key] = index
                return d

        def _create_matrix(self, dict):
                size = len(dict)
                ndarray = np.array(np.zeros((size, size)))
                print(np.shape(ndarray))

                return ndarray
                

        def fill_matrix_vector(self, matrix, words, dict, window):
                neighbors_qty = window//2
                n = len(words)

                #on parcours chaque mot du texte
                for i in range(n):
                        #On trouve l'index de ce mot dans le dict
                        index = dict[words[i]]
                        #On trouve les voisins avant
                        for offset in range(-neighbors_qty, neighbors_qty+1):
                                #Empecher le outofbound
                                if offset == 0:
                                        continue

                                j = i + offset

                        #On trouve les voisins après
                                if 0 <= j < n:
                                        neighbor = words[j]
                                        idx = dict[neighbor]
                                        matrix[index, idx] += 1
                return matrix





        
