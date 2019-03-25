from .board import Board
from .grid import Grid, TOTAL_NUM_GREENS
from random import randint

_NUM_TURNS = 9


class Game:
    def __init__(self, rand_turn=False):
        self._board, self._grid = Board(), Grid()
        self._greens_remaining = TOTAL_NUM_GREENS
        self._turn = 1 # player two always gives the clue first
        self._turns_remaining = _NUM_TURNS
        self._black_guessed = False
        
        if rand_turn: self._turn = randint(1, 2)
        
    def guess(self, word):
        if self._game_state() != "ongoing": return
        r, c = self._board.word_location(word)
        if r == -1 and c == -1: return
        
        # see if it's already been picked
        co = self._board.get_cover(r, c)
        if co and co in "bg" + str(self._turn): return
            
        if self._turn == 1: color = self._grid.get_p2_color(r, c)
        else: color = self._grid.get_p1_color(r, c)
        
        if color == "g": 
            self._board.correct_guess(r, c)
            self._greens_remaining -= 1
        elif color == "b": 
            self._board.black_guess(r, c)
            self._black_guessed = True
            self.turn_complete()
        else: 
            if self._turn == 1: self._board.p1_incorrect_guess(r, c)
            else: self._board.p2_incorrect_guess(r, c)
            self.turn_complete()
            
    def get_turn(self):
        return self._turn
    
    def turn_complete(self):
        self._turns_remaining -= 1
        old_turn = self._turn
        self._turn = 1 if old_turn == 2 else 2
        
#        for r in range(5):
#            for c in range(5):
#                cg = self._grid.get_color(r, c, old_turn)
#                cb = self._board.get_cover(r, c)
#                if cg == "g" and cb != "g": return
#                
#        self._turn = old_turn
        
    def _game_state(self):
        if self._greens_remaining == 0: return "victory"
        elif self._black_guessed or not self._turns_remaining: return "defeat"
        else: return "ongoing"
        
    def get_update_info(self):
        return {
            "turns_remaining": self._turns_remaining,
            "greens_remaining": self._greens_remaining,
            "turn": self._turn,
            "covers": self._board.get_covers(),
            "game_state": self._game_state()
        }
    
    def get_game_info(self, player):
        d = self.get_update_info()
        d.update({
            "words": self._board.get_words(),
            "grid": self._grid.display_p1() if player == 1 
                    else self._grid.display_p2(),
            "player": player
        })
        return d
    
    def new_game(self):
        self.__init__(True)
        
    