from random import sample, shuffle

def random_words():
    """ Choose 25 random words from words.txt """
    with open("words/words.txt") as f: l = sample(f.read().upper().split(), 25)
    shuffle(l)
    return l