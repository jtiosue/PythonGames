import copy

class Board(object):
    def __init__(self, grid):
        self.grid = grid
        self.soln = False

    def get_value(self, row, column):
        return self.grid[row][column]

    def set_value(self, row, column, value):
        self.grid[row][column] = value

    @staticmethod
    def neighbors(row, column):
        topR, topC = 3 * (row // 3), 3 * (column // 3)
        for r in range(topR, topR + 3):
            for c in range(topC, topC + 3):
                if r != row or c != column:
                    yield r, c

    def is_valid(self, row, column, value):
        return all((
                all((value != self.get_value(row, c) for c in range(9))),
                all((value != self.get_value(r, column) for r in range(9))),
                all((value != self.get_value(r, c) for r, c in
                                                Board.neighbors(row, column)))
        ))

    def find_next(self):
        for r in range(9):
            for c in range(9):
                if not self.get_value(r, c):
                    return r, c
        return -1, -1

    def __iter__(self):
        for r in range(9):
            for c in range(9):
                yield self.get_value(r, c)

    def solve(self):
        r, c = self.find_next()
        if r == -1 or c == -1: return True
        for v in range(1, 10):
            if self.is_valid(r, c, v):
                self.set_value(r, c, v)
                if self.solve():
                    return True
        self.set_value(r, c, 0)
        return False

    def solution(self):
        if not self.soln:
            self.soln = Board(copy.deepcopy(self.grid))
            self.soln.solve()
        return self.soln

    def __str__(self):
        l = [" ".join([str(row[i:i+3]) for i in range(0, 9, 3)])
                                                       for row in self.grid]
        return "\n\n".join(["\n".join(l[i:i+3]) for i in range(0, 9, 3)])

if __name__ == "__main__":
    # input = [
        # [5,1,7,6,0,0,0,3,4],
        # [2,8,9,0,0,4,0,0,0],
        # [3,4,6,2,0,5,0,9,0],
        # [6,0,2,0,0,0,0,1,0],
        # [0,3,8,0,0,6,0,4,7],
        # [0,0,0,0,0,0,0,0,0],
        # [0,9,0,0,0,0,0,7,8],
        # [7,0,3,4,0,0,5,6,0],
        # [0,0,0,0,0,0,0,0,0]
    # ]
    input = [ # world's hardest sudoku
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ]
    b = Board(input)
    print(b)
    print("\nsolved by\n")
    print(b.solution())