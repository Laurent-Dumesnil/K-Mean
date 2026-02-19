import numpy as np

class Prediction():
    def __init__(self, train, word, synonym_count, method):
        self.word = word
        self.train = train
        if self.word not in self.train.dict:
            raise ValueError("Le mot recherché n'est pas dans le texte")
        try:
            self.synonym_count = int(synonym_count)
            if self.synonym_count <= 0:
                raise ValueError('Votre nombre de synonyme doit être plus grand que 1')
            elif self.synonym_count >= len(self.train.dict):
                raise ValueError('Votre nombre de synonyme ne peut pas être plus grand que le nombre de mot du texte')

            self.method = int(method)
        except:
            raise ValueError('Vous devez entrez un nombre entier comme deuxième et troisième paramètres')

        self.stop_words = ["le", "la", "les", "l", "un", "une", "des",
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
        
        self.index_of_word = self.train.dict[self.word]

        match self.method:
            case 1:
                self.result = self.dot_product()
            case 2:
                self.result = self.least_squares()
            case 3:
                self.result = self.city_block()
            case _:
                raise ValueError('Votre méthode doit être inclus entre 1 et 3')

    def dot_product(self):
        product_matrix = self.train.matrix[self.index_of_word]*self.train.matrix
        results = np.sum(product_matrix, axis=1)

        return self.build_results(results, False)

    def least_squares(self):
        words_to_compare = self.train.matrix[self.index_of_word , :]
        compared_words = (self.train.matrix[:] - words_to_compare) ** 2
        results = np.sum(compared_words, axis=1)

        return self.build_results(results)
    
    def city_block(self):
        return {}
    
    def build_results(self, result_tab, ascending = True):
        idx_results = np.argsort(result_tab)
        if not ascending:
            idx_results = np.flip(idx_results)

        result_dict = {}

        i = 0
        j = 0
        while i < self.synonym_count and j < len(self.train.lookup_table)-1:
            if self.train.lookup_table[idx_results[j+1]] not in self.stop_words:
                result_dict[self.train.lookup_table[idx_results[j+1]]] = result_tab[idx_results[j+1]]
                i = i + 1
            j = j + 1 

        return result_dict
