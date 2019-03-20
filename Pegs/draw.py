import game
import tkinter as tk

BLACK = "black"
BG = "#dedfe0"
CUSHION = 3


def apply_cushion(*rect_def, cushion=CUSHION):
    x0, y0, x1, y1 = rect_def
    return x0 + CUSHION, y0 + CUSHION, x1 - CUSHION, y1 - CUSHION


def draw_cir(canvas, *rect_def):
    canvas.create_oval(*rect_def, fill=BG)


def draw_box(canvas, *rect_def):
    canvas.create_rectangle(*rect_def, fill=BG)


def draw_hol(canvas, *rect_def):
    canvas.create_rectangle(*rect_def, fill=BLACK)


def draw_plu(canvas, *rect_def):
    x0, y0, x1, y1 = rect_def
    xm, ym = (x0 + x1) // 2, (y0 + y1) // 2
    canvas.create_line(xm, y0, xm, y1)
    canvas.create_line(x0, ym, x1, ym)


def draw_tri(canvas, *rect_def):
    x0, y0, x1, y1 = rect_def
    canvas.create_polygon(x0, y0, x0, y1, x1, y1, fill=BG, outline=BLACK)


def draw_uni(canvas, *rect_def):
    x0, y0, x1, y1 = rect_def
    xm, ym = (x0 + x1) // 2, (y0 + y1) // 2
    canvas.create_polygon(x0, ym, xm, y0, x1, ym, xm, y1,
                          fill=BG, outline=BLACK)
    draw_plu(canvas, *rect_def)
    draw_cir(canvas, (x0+xm)//2, (y0+ym)//2, (x1+xm)//2, (y1+ym)//2)


def draw_wal(canvas, *rect_def):
    for f in (draw_box, draw_plu):
        f(canvas, *rect_def)
    canvas.create_line(*rect_def)
    x0, y0, x1, y1 = rect_def
    canvas.create_line(x1, y0, x0, y1)


def draw_player(canvas, *rect_def):
    draw_plu(canvas, *rect_def)
    x0, y0, x1, y1 = rect_def
    xt, yt = (x1 - x0) // 3, (y1 - y0) // 3
    canvas.create_line(x0+xt, y0, x1-xt, y0, width=CUSHION)
    canvas.create_line(x0+xt, y1, x1-xt, y1, width=CUSHION)
    canvas.create_line(x0, y0+yt, x0, y1-yt, width=CUSHION)
    canvas.create_line(x1, y0+yt, x1, y1-yt, width=CUSHION)


DRAW = {
    game.cir: draw_cir, game.box: draw_box, game.plu: draw_plu,
    game.tri: draw_tri, game.uni: draw_uni, game.hol: draw_hol,
    game.wal: draw_wal, game.player: draw_player
}


class Canvas(tk.Canvas):
    """
    Inherits from tk.Canvas. ASSUMES THAT draw_board(self, board) IS CALLED
    FIRST SO AS TO INITIALIZE self.dr AND self.dc.
    """
    def draw_board(self, board):
        """
        Draw board on canvas.

        :param board: (game.Board object), board to draw.
        :return: None
        """
        self.update()
        w, h = self.winfo_width(), self.winfo_height()
        self.dc, self.dr = w // board.cols, h // board.rows
        update_dict = {pos: board.get_value(pos) for pos in board.all_index()}
        self.redraw(update_dict)

    def clear(self, x0, y0, x1, y1):
        """
        Clear on Canvas element drawn within the given rectangular.

        :param x0, y0, x1, y1: (int), rectangular definition to clear.
        :return: None.
        """
        for element in self.find_enclosed(x0, y0, x1, y1):
            self.delete(element)

    def rect_def(self, pos):
        """
        Convert grid position to pixle position.

        :param pos: (tuple), (r, c).
        :return: (tuple of ints), rectangular definition.
        """
        r, c = pos
        x0, y0 = self.dc * c, self.dr * r
        x1, y1 = x0 + self.dc, y0 + self.dr
        return x0, y0, x1, y1

    def redraw(self, update_dict):
        """
        Clear positions and draw their new values.

        :param update_dict: (dict), positions that need to be redrawn.
        :return: None.
        """
        for (k, i) in update_dict.items():
            rect_def = self.rect_def(k)
            self.clear(*rect_def)
            if i in DRAW:
                DRAW[i](self, *apply_cushion(*rect_def))


if __name__ == '__main__':
    import sys
    if not sys.argv[1:]:
        filename = "levels/test.txt"
    else:
        name = sys.argv[-1]
        if len(name.split(".")) == 1:
            name += ".txt"
        filename = "levels/" + name
    root = tk.Tk()
    root.geometry("400x400")
    root.bind("<Escape>", lambda e: root.destroy())
    board = game.make_board(filename)
    canvas = Canvas(root, bg=BG)
    canvas.pack(expand=tk.TRUE, fill=tk.BOTH)
    canvas.draw_board(board)
    root.mainloop()
