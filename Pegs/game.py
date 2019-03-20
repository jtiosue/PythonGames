"""
Pegs, the game.

This file contains the structure of the game, as well
as a simple text based implementation of the game.

Game files must be of the form:
    dimensions=(r, c), player=(r, c),
    circle=[(r, c), (r, c), ...],
    ...
"""

PIECES = box, cir, plu, tri, uni = (
    "box", "circle", "plus", "triangle", "universal"
)
OTHER = hol, wal, player, bla = "hole", "wall", "player", "blank"
ALL_PIECES = PIECES + OTHER
STRINGS = {
    box: "B", cir: "O", plu: "+", tri: "T", uni: "U",
    hol: "H", wal: "W", bla: " ", player: "P"
}

COLLISION_RULES = {
    (box, box): bla, (box, hol): bla, (box, uni): bla, (box, bla): box,
    (cir, cir): bla, (cir, hol): hol, (cir, uni): bla, (cir, bla): cir,
    (plu, plu): uni, (plu, hol): hol, (plu, uni): uni, (plu, bla): plu,
    (tri, tri): wal, (tri, hol): hol, (tri, uni): wal, (tri, bla): tri,
    (uni, uni): wal, (uni, hol): bla, (uni, box): bla, (uni, bla): uni,
    (uni, cir): bla, (uni, plu): uni, (uni, tri): wal
}

DIMENSIONS = "dimensions"
DEFEAT, ONGOING, VICTORY = "Defeat", "Ongoing", "Victory"


class Player(object):
    """ Hold information about the position of the player """
    def __init__(self, pos):
        """
        :param pos: (tuple or list), (r, c).
        """
        self.pos = pos

    def move(self, direc):
        """
        Find the next two squares in the direction of 'direc'.

        :param direc: (tuple or list).
        :return: (list of tuples), [next position 1, next position 2].
        """
        x, y = direc
        r, c = self.pos
        return [(r+x, c+y), (r+2*x, c+2*y)]

    def update(self, pos):
        """
        Update the position of player.

        :param pos: (tuple or list), (r, c).
        :return: None.
        """
        self.pos = pos


class Board(object):
    """
    Handles all actions and information of the game board.
    """
    left, right, up, down = (0, -1), (0, 1), (-1, 0), (1, 0)

    def __init__(self, board, player):
        """
        :param board: (2d list), rows and columns with respective pieces.
        :param player: (Player object).
        """
        self.rows, self.cols = len(board), len(board[0])
        self.board, self.player = board, player

    def on_board(self, pos):
        """
        Find whether pos is within the bounds of the board.

        :param pos: (tuple or list), (r, c).
        :return: (bool), True or False.
        """
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def get_value(self, pos, default=wal):
        """
        Find the value that is at position pos. If pos is not a valid position,
        return default.

        :param pos: (tuple or list), (r, c).
        :param default: (str), value to return if pos is invalid.
        :return: (str), value.
        """
        if self.on_board(pos):
            r, c = pos
            return self.board[r][c]
        else:
            return default

    def set_value(self, pos, value=bla):
        """
        Set the value on the board at pos to value.

        :param pos: (tuple or list), (r, c).
        :param value: (str), value to input to board.
        :return: None.
        """
        if self.on_board(pos):
            r, c = pos
            self.board[r][c] = value

    def update_player(self, pos):
        """
        Make the player's current position blank and move him to pos.

        :param pos: (tuple or list), (r, c).
        :return: None.
        """
        self.set_value(self.player.pos)
        self.set_value(pos, player)
        self.player.update(pos)

    def collision(self, s1, s2):
        """
        Handle the player trying to move to s1.

        :param s1: (tuple or list), (r, c) of next position 1.
        :param s2: (tuple or list), (r, c) of next position 2.
        :return: (dict), positions that changed mapping to their new values.
        """
        s1_v, s2_v = self.get_value(s1), self.get_value(s2)
        if s1_v == bla:
            update_dict = {self.player.pos: bla, s1: player}
            self.update_player(s1)
        elif s1_v == hol:
            update_dict = {self.player.pos: bla}
            self.update_player((-1, -1))
        elif (s1_v, s2_v) in COLLISION_RULES:
            new = COLLISION_RULES[(s1_v, s2_v)]
            update_dict = {self.player.pos: bla, s1: player, s2: new}
            self.update_player(s1)
            self.set_value(s2, new)
        else:
            update_dict = {}
        return update_dict

    def move(self, direction):
        """
        Try to move the player in direction 'direction'.

        :param direction: (tuple or list), (delta r, delta c).
        :return: (dict), positions that changed mapping to their new values.
        """
        return self.collision(*self.player.move(direction))

    def all_index(self):
        """
        Generate all the valid positions on the board.

        :yield: (tuple), (r, c).
        """
        for r in range(self.rows):
            for c in range(self.cols):
                yield r, c

    def __iter__(self):
        """
        Generate all the values in the board.

        :yield: (str), values in board.
        """
        for p in self.all_index():
            yield self.get_value(p)

    def state(self):
        """
        Determine the state of the board.

        :return: (str), DEFEAT, VICTORY, or ONGOING.
        """
        if not self.on_board(self.player.pos): return DEFEAT
        elif not any((s in PIECES for s in self)): return VICTORY
        else: return ONGOING

    def __str__(self):
        """
        :return: (str), string representation of the board.
        """
        return "\n".join(
            [" ".join(map(lambda p: STRINGS[p], row)) for row in self.board]
        )

    @staticmethod
    def make_board(dimensions, **kwargs):
        """
        Make a board object with the information provided.

        :param dimensions: (tuple or list), (rows, columns).
        :param kwargs: {player: (r, c), piece1: [(r, c), ...], ...}
        :return: (Board object).
        """
        rows, cols = dimensions
        b = [[bla for _ in range(cols)] for _ in range(rows)]
        p = Player(kwargs.pop(player))
        board = Board(b, p)
        for piece in kwargs:
            for pos in kwargs[piece]:
                board.set_value(pos, piece)
        board.set_value(p.pos, player)
        return board


def read_file(filename):
    """
    Extract game data from file.

    :param filename: (str), filename of game.
    :return: (tuple): (tuple, dict), (dimensions, {player: (r, c), ...})
    """
    with open(filename) as f:
        game = eval("dict(%s)" % f.read().strip())
    dimensions = game.pop(DIMENSIONS)
    return dimensions, game


def make_board(filename):
    """
    Make board from data from file.

    :param filename: (str), name of file to read from to get game data.
    :return: None.
    """
    dim, kwargs = read_file(filename)
    return Board.make_board(dim, **kwargs)


def play_text(filename):
    """
    Play a text based version of the game with the given information.

    :param filename: (str), name of file to read from to get game data.
    :return: None.
    """
    board = make_board(filename)
    keys = {"a": Board.left, "d": Board.right, "w": Board.up, "s": Board.down}
    print("Controls: %s" % str(list(keys.keys())))
    while board.state() == ONGOING:
        print(board)
        for i in str(input("Enter move: ")):
            if i in keys: board.move(keys[i])
    print(board)
    print(board.state())


if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        filenames = ["test.txt"]
    else:
        filenames = sys.argv[1:]
    for filename in filenames:
        if len(filename.split(".")) > 1:
            play_text("levels/" + filename)
        else:
            play_text("levels/" + filename + ".txt")