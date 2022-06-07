from words import random_words

class Board:
    """ Deal with the words on the board """
    def __init__(self):
        """ initialize 25 random words and empty covers """
        self._words, self._cover = random_words(), [""] * 25
        self._words_dict = {
            self.get_word(r, c): (r, c) for r in range(5) for c in range(5)
        }
        
    def _get_index(self, row, col):
        if row not in range(5) or col not in range(5):
            raise ValueError("Row or Column out of range")
        return 5*row + col
    
    def get_word(self, row, col):
        return self._words[self._get_index(row, col)]
    
    def word_location(self, word):
        return self._words_dict.get(word, (-1, -1))
    
    def get_cover(self, row, col):
        return self._cover[self._get_index(row, col)]
    
    def correct_guess(self, row, col):
        self._cover[self._get_index(row, col)] = "g"
        
    def p1_incorrect_guess(self, row, col):
        if self._cover[self._get_index(row, col)] == "2":
            self._cover[self._get_index(row, col)] = "3"
        else:
            self._cover[self._get_index(row, col)] = "1"
        
    def p2_incorrect_guess(self, row, col):
        if self._cover[self._get_index(row, col)] == "1":
            self._cover[self._get_index(row, col)] = "3"
        else:
            self._cover[self._get_index(row, col)] = "2"
        
    def black_guess(self, row, col):
        self._cover[self._get_index(row, col)] = "b"
        
    def get_words(self):
        return self._words
    
    def get_covers(self):
        return self._cover

    def __str__(self):
        return "words: " + str(self._words) + "\ncovers: " + str(self._cover)
