import numpy as np

STOP_WORDS = ["le", "la", "les", "l", "un", "une", "des",
                    "mon", "ton", "son", "ma", "ta", "sa",
                    "mes", "tes", "ses", "notre", "votre", "leur",
                    "nos", "vos", "leurs", "ce", "cette", "ces",
                    "à", "de", "du", "au", "aux", "dans", "sur",
                    "pour", "par", "en", "avec", "chez", "contre",
                    "entre", "vers", "avant", "après", "et", "ou",
                    "mais", "ni", "que", "car", "je", "tu", "il",
                    "elle", "on", "nous", "vous", "ils", "elles",
                    "me", "te", "se", "lui", "moi", "toi", "soi",
                    "eux", "pas", "plus", "tout", "tous", "rien",
                    "oui", "non", "ne", "très", "déjà", "aussi",
                    "celui", "celle", "ceux", "celles", "ceci", "cela", "ça",
                    "s","d","j","t","m","n","c","y","que","qu","qui", "était",
                    "avait", "si", "sans", "étaient", "avaient", "comme"]

class Prediction():
    def __init__(self, train):
        self.__train = train
        self.__word = None
        self.__synonym_count = None
        self.__method = None
        self.__index_of_word = None
            
    def predict(self, synonym_count, method):
        self.synonym_count = synonym_count
        self.method = method
        self.__index_of_word = self.__train.word_dict[self.__word]
        match self.method:
            case 1:
                return self.__dot_product()
            case 2:
                return self.__least_squares()
            case 3:
                return self.__city_block()
            case _:
                return None
    

    def __dot_product(self):
        product_matrix = self.__train.coocurence_matrix[self.__index_of_word]*self.__train.coocurence_matrix
        results = np.sum(product_matrix, axis=1)

        return self.__build_results(results, False)

    def __least_squares(self):
        words_to_compare = self.__train.coocurence_matrix[self.__index_of_word , :]
        compared_words = (self.__train.coocurence_matrix[:] - words_to_compare) ** 2
        results = np.sum(compared_words, axis=1)

        return self.__build_results(results)
    
    def __city_block(self):
        words_to_compare = self.__train.coocurence_matrix[self.__index_of_word, :]
        compared_words = np.abs(self.__train.coocurence_matrix[:] - words_to_compare)
        results = np.sum(compared_words, axis=1)

        return self.__build_results(results)
        
    #Fonction utilitaire construisant le dictionnaire de résultat, utilisable par toutes les stratégies
    def __build_results(self, result_tab, ascending = True):
        #Trie les index des résultats dans l'ordre approprié
        idx_results = np.argsort(result_tab)
        if not ascending:
            idx_results = np.flip(idx_results)

        result_dict = {}

        #Rempli le dictionnaire de résultat. Les clés sont les valeurs trouvées en mots, les valeurs
        #sont les valeurs associées par l'algorithme utilisé. Les stop-words sont ignorés et
        #une protectione contre les boucles infinies est établie si pas assez de mot sont trouvés
        i = 0
        j = 0
        while i < self.__synonym_count and j < len(self.__train.lookup_table)-1:
            if self.__train.lookup_table[idx_results[j+1]] not in STOP_WORDS:
                result_dict[self.__train.lookup_table[idx_results[j+1]]] = result_tab[idx_results[j+1]]
                i = i + 1
            j = j + 1 

        return result_dict
    
    @property
    def word(self):
        return self.__word
    
    @word.setter
    def word(self, word):
        if word not in self.__train.word_dict:
            raise ValueError("\nLe mot recherché n'est pas dans le texte")
        self.__word = word

    @property
    def synonym_count(self):
        return self.__synonym_count
    
    @synonym_count.setter
    def synonym_count(self, synonym_count):
        if synonym_count <= 0:
            raise ValueError('\nVotre nombre de synonyme doit être plus grand que 0')
        elif synonym_count >= len(self.__train.word_dict):
            raise ValueError('\nVotre nombre de synonyme ne peut pas être plus grand que le nombre de mot du texte')
        self.__synonym_count = synonym_count

    @property
    def method(self):
        return self.__method
    
    @method.setter
    def method(self, method):
        if method < 1 or method > 3:
            raise ValueError('\nVotre méthode doit être inclus entre 1 et 3')
        self.__method = method
