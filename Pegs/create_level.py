import game, draw, main
import tkinter as tk


CLICK, RESET, COMPLETE = "Button-1", "Return", "space"


class Maker(tk.Frame):
    """ Inherits from tk.Frame. Draws pieces where user clicks """
    def __init__(self, *args, **kwargs):
        """

        :param args: a tk.Tk window must be the first argument in args.
        :param kwargs: a dimension must be in kwargs (dimensions=(r, c)).
        """
        dimensions = kwargs.pop(game.DIMENSIONS)
        super().__init__(*args, **kwargs)
        self.board = game.Board.make_board(dimensions, player=(-1, -1))
        self.can = draw.Canvas(self, bg=draw.BG)
        self.can.pack(expand=tk.TRUE, fill=tk.BOTH)

        args[0].bind("<%s>" % CLICK, self.click)

    def pack(self, *args, **kwargs):
        """ Draws board in addition to performing the super method """
        super().pack(*args, **kwargs)
        self.can.draw_board(self.board)

    def position(self, *pos):
        """
        Convert pixel position to grid position.

        :param pos: (ints), pixel position.
        :return: (tuple), (r, c) grid position.
        """
        x, y = pos
        return y // self.can.dr, x // self.can.dc

    def click(self, event):
        """
        Draws a piece at the location of event.

        :param event: (tk event).
        :return: None.
        """
        pos = self.position(event.x, event.y)
        i = game.ALL_PIECES.index(self.board.get_value(pos)) + 1
        self.draw(pos, game.ALL_PIECES[i % len(game.ALL_PIECES)])

    def draw(self, pos, value):
        """
        Draw the value at pos and update the board.

        :param pos: (tuple), (r, c) grid position.
        :param value: (str), value to draw at position.
        :return: None.
        """
        self.board.set_value(pos, value)
        self.can.redraw({pos: value})


def write_board(board, filename):
    """
    Write board to file as dictionary.

    :param board: (game.Board object), board to write to file.
    :param filename: (str), file to write to.
    :return: None.
    """
    pieces = {game.DIMENSIONS: (board.rows, board.cols)}
    for pos in board.all_index():
        v = board.get_value(pos)
        if v == game.player:
            pieces[v] = pos
        elif v != game.bla:
            pieces.setdefault(v, []).append(pos)

    if len(filename.split(".")) == 1:
        filename += ".txt"
    filename = "levels/" + filename
    with open(filename, "w") as f:
        f.write(str(pieces))


def draw_board(dimensions, filename):
    """
    Open the maker and handle resets, cancels, and completion.

    :param dimensions: (tuple), (r, c).
    :param filename: (str), filename to write to.
    :return: None.
    """
    root = tk.Tk()
    root.title("dimensions: %s, level: %s" % (str(dimensions), filename))
    root.geometry("400x400")
    frame = Maker(root, dimensions=dimensions)
    frame.pack(expand=tk.TRUE, fill=tk.BOTH)
    def reset():
        frame.destroy()
        frame.__init__(root, dimensions=dimensions)
        frame.pack(expand=tk.TRUE, fill=tk.BOTH)
    def write():
        root.destroy()
        write_board(frame.board, filename)
        print("Board saved.")
        print(frame.board)

    root.bind("<%s>" % RESET, lambda e: reset())
    root.bind("<%s>" % COMPLETE, lambda e: write())
    root.bind("<Escape>", lambda e: root.destroy())
    root.mainloop()


if __name__ == '__main__':
    import sys
    next_filename = str(
        int(main.get_name_from_path(main.get_levels()[-1]).split(".")[0]) + 1
    )
    a = sys.argv[1:]
    if not a or len(a) == 1:
        dimensions, filename = (8, 12), next_filename
    elif len(a) == 2:
        dimensions, filename = a, next_filename
    else:
        dimensions, filename = a[-3:-1], a[-1]

    try:
        draw_board([int(x) for x in dimensions], filename)
    except Exception as e:
        print(e)
        print(
            "\nRun with: 'python %s (rows) (cols) (filename)'" % sys.argv[0]
        )
