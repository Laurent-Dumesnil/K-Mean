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
                    "celui", "celle", "ceux", "celles", "ceci", "cela", "ça"
                    ,"s","d","j","t","m","n","c","y","que","qu","qui"]

class Prediction():
    def __init__(self, _train):
        self._train = _train
        self._word = None
        self._synonym_count = None
        self._method = None
        self._index_of_word = None
            
    def predict(self):
        self._index_of_word = self._train.word_dict[self._word]
        match self.method:
            case 1:
                return self._dot_product()
            case 2:
                return self._least_squares()
            case 3:
                return self._city_block()
            case _:
                return None
    

    def _dot_product(self):
        product_matrix = self._train.coocurence_matrix[self._index_of_word]*self._train.coocurence_matrix
        results = np.sum(product_matrix, axis=1)

        return self._build_results(results, False)

    def _least_squares(self):
        words_to_compare = self._train.coocurence_matrix[self._index_of_word , :]
        compared_words = (self._train.coocurence_matrix[:] - words_to_compare) ** 2
        results = np.sum(compared_words, axis=1)

        return self._build_results(results)
    
    def _city_block(self):
        words_to_compare = self._train.coocurence_matrix[self._index_of_word, :]
        compared_words = np.abs(self._train.coocurence_matrix[:] - words_to_compare)
        results = np.sum(compared_words, axis=1)

        return self._build_results(results)
        
    #Fonction utilitaire construisant le dictionnaire de résultat, utilisable par toutes les stratégies
    def _build_results(self, result_tab, ascending = True):
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
        while i < self._synonym_count and j < len(self._train.lookup_table)-1:
            if self._train.lookup_table[idx_results[j+1]] not in STOP_WORDS:
                result_dict[self._train.lookup_table[idx_results[j+1]]] = result_tab[idx_results[j+1]]
                i = i + 1
            j = j + 1 

        return result_dict
    
    @property
    def word(self):
        return self._word
    
    @word.setter
    def word(self, word):
        if word not in self._train.word_dict:
            raise ValueError("\nLe mot recherché n'est pas dans le texte")
        self._word = word

    @property
    def synonym_count(self):
        return self._synonym_count
    
    @synonym_count.setter
    def synonym_count(self, synonym_count):
        if synonym_count <= 0:
            raise ValueError('\nVotre nombre de synonyme doit être plus grand que 1')
        elif synonym_count >= len(self._train.word_dict):
            raise ValueError('\nVotre nombre de synonyme ne peut pas être plus grand que le nombre de mot du texte')
        self._synonym_count = synonym_count

    @property
    def method(self):
        return self._method
    
    @method.setter
    def method(self, method):
        if method < 1 or method > 3:
            raise ValueError('\nVotre méthode doit être inclus entre 1 et 3')
        self._method = method
