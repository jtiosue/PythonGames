import random

class Board:
    WIN = (
        ((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
        ((0, 0), (1, 1), (2, 2)), ((2, 0), (1, 1), (0, 2)),
    )
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def __str__(self):
        return "\n" + "\n".join([" | ".join(x) for x in self.board]) + "\n"

    def is_valid(self, pos):
        return self.get_item(pos) == " "

    def all_moves(self):
        yield from ((r, c) for r in range(3) for c in range(3)
                    if self.is_valid((r, c)))

    def state(self):
        for p in Board.WIN:
            for i in ("X", "O"):
                if all((self.get_item(x) == i for x in p)): return i
        try:
            next(self.all_moves())
            return "ongoing"
        except StopIteration: return "draw"
        
    def get_item(self, pos):
        return self.board[pos[0]][pos[1]]

    def set_item(self, pos, piece):
        self.board[pos[0]][pos[1]] = piece


def pick_next(board, player, count=0):
    def pick_next_help(board, player, count):
        other = "X" if player == "O" else "O"
        s = board.state()
        if s == player: return (), 10, count
        elif s == other: return (), -10, count
        count += 1
        best = False
        for (r, c) in board.all_moves():
            board.set_item((r, c), player)
            _, s, co = pick_next_help(board, other, count)
            s *= -1

            if (not best or s > best[1] or (s == best[1] and (
                (s >= 0 and co < best[2]) or (s < 0 and co > best[2])
            ))): best = (r, c), s, co

            board.set_item((r, c), " ")

        if best: return best
        else: return (), 0, count
    return pick_next_help(board, player, count)[0]


def play(first=True):
    board, i = Board(), 0
    if not first:
        board.set_item(random.choice([(0, 0), (0, 2), (2, 0), (2, 2)]), "X")
    first = "X" if first else "O"
    other = "X" if first == "O" else "O"
    while board.state() == "ongoing":
        i += 1
        print(board)
        if i % 2:
            s = input("Row, Col: ")
            r, c = int(s[0]), int(s[1])
            if board.is_valid((r, c)): board.set_item((r, c), first)
            else: i -= 1
        else: board.set_item(pick_next(board, other), other)
    print(board)
    print(board.state())


if __name__ == '__main__':
    import sys
    play(not bool(sys.argv[1:]))
