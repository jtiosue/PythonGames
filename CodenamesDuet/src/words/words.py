from random import sample, shuffle

def random_words():
    """ Choose 25 random words from words.txt """
    with open("words/words.txt") as f: 
        l = [
            x.strip()
            for x in sample(f.read().upper().split("\n"), 25)
        ]
    shuffle(l)
    return l
