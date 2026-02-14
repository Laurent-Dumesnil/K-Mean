from sys import argv
import re
import numpy as np

class Training():

        @staticmethod
        def read_text(file, encode):
                f = open(file, encoding=encode)
                text = f.read()
                f.close()

                return text
        
        @staticmethod
        def extract_words(text):
                words = re.findall(r"\b\w+\b", text.lower())
                d =  dict.fromkeys(words)
                index = 0

                for index, key in enumerate(d):
                        d[key] = index
                return d

        def _create_matrix(dict):
                size = len(dict)
                ndarray = np.array(np.zeros((size, size)))
                print(np.shape(ndarray))

                return ndarray
        
        @staticmethod
        def fill_matrix_vector(text, dict, window):
                matrix = Training._create_matrix(dict)
                words = re.findall(r'\b\w+\b', text.lower())
                neighbors_qty = window//2

                #on parcours chaque mot du texte
                for i in range(len(words)):
                        #On trouve l'index de ce mot dans le dict
                        index = dict[words[i]]
                        #On trouve les voisins avant
                        count = -1
                        for _ in range(1, neighbors_qty+1):
                                #Empecher le outofbound
                                if i+count < 0:
                                        count -= 1
                                        continue

                                neighbor = words[i+count]
                                idx = dict[neighbor]
                                matrix[index, idx] += 1
                                count -= 1

                        #On trouve les voisins après
                        count = 1
                        for _ in range(1, neighbors_qty+1):
                                #Empecher le outofbound
                                if i+count >= len(words):
                                        count += 1
                                        continue

                                neighbor = words[i+count]
                                idx = dict[neighbor]
                                matrix[index, idx] += 1
                                count += 1

                return matrix





        
