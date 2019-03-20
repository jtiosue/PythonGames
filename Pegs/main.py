import tkinter as tk
import os, game, draw


CONTROLS = LEFT, RIGHT, UP, DOWN = "Left", "Right", "Up", "Down"
RESET = "Return"

DIRECTIONS = {
    LEFT: game.Board.left, RIGHT: game.Board.right,
    UP: game.Board.up, DOWN: game.Board.down
}

FONTSIZE = 20
FONT = "ms %d" % FONTSIZE
FONTCOLOR = "white"

def get_name_from_path(path):
    """
    Return just the filename from its full path.

    :param path: (str), directory path.
    :return: (str), name of file.
    """
    filename = path.split("/")[-1]
    return filename.split(".")[0]


def get_levels(default=["test.txt"]):
    """
    Find all integer named level filenames.

    :return: (list), sorted list of level filenames.
    """
    key = lambda f: int(f.split(".")[0])
    levels = []
    for f in os.listdir("levels"):
        try:
            key(f)
            levels.append(f)
        except ValueError:
            pass
    levels.sort(key=key)
    if not levels:
        levels = default
    return ["levels/" + l for l in levels]


class Level(tk.Frame):
    """
    Inherits from tk.Frame. Pack a level onto a main window.
    """
    levels = get_levels()

    def __init__(self, master, level=0):
        """
        :param master: (tk.Tk window), main window.
        :param level: (int), index of current level in Level.levels.
        """
        super().__init__(master)
        master.title("Pegs: Level " + get_name_from_path(Level.levels[level]))
        self.can = draw.Canvas(self, bg=draw.BG)
        self.can.pack(expand=tk.TRUE, fill=tk.BOTH)

        for key in CONTROLS:
            master.bind("<%s>" % key, self.move)

        self.board = game.make_board(Level.levels[level])

        self.master, self.level = master, level

    def pack(self, *args, **kwargs):
        """ Adds to the super method to draw board """
        super().pack(*args, **kwargs)
        self.can.draw_board(self.board)

    def unbind_controls(self):
        """ Take away control from the player """
        for key in CONTROLS:
            self.master.unbind("<%s>" % key)

    def create_message(self, message):
        """ Draw a message in the middle of the canvas """
        w, h = self.can.winfo_width(), self.can.winfo_height()
        self.can.create_text(w//2, h//2,
                             text=message, font=FONT, fill=FONTCOLOR)

    def move(self, event):
        """
        Update game and redraw board based on player's move.

        :param event: (tk keystroke event).
        :return: None.
        """
        update_dict = self.board.move(DIRECTIONS[event.keysym])
        if not update_dict: return
        self.can.redraw(update_dict)

        state = self.board.state()
        if state == game.VICTORY:
            if self.level + 1 < len(Level.levels):
                self.level += 1
            else:
                self.level = 0
                state += ". You beat the game!"
            self.create_message(state)
            self.unbind_controls()
        elif state == game.DEFEAT:
            self.unbind_controls()
            self.create_message(state)


def play(level=0):
    """
    Create a tk.Tk window and pack the game on it.

    :param level: (int), index of current level in Level.levels.
    :return: None.
    """
    root = tk.Tk()
    root.geometry("400x400")
    frame = Level(root, level)
    frame.pack(expand=tk.TRUE, fill=tk.BOTH)
    def reset():
        l = frame.level
        frame.destroy()
        frame.__init__(root, l)
        frame.pack(expand=tk.TRUE, fill=tk.BOTH)

    root.bind("<%s>" % RESET, lambda e: reset())
    root.bind("<Escape>", lambda e: root.destroy())
    root.mainloop()


if __name__ == '__main__':
    import sys
    if not sys.argv[1:]: play()
    else:
        l = "levels/" + sys.argv[-1]
        try:
            if len(l.split(".")) > 1:
                level = Level.levels.index(l)
            else:
                l += ".txt"
                level = Level.levels.index(l)
            play(level)
        except ValueError:
            Level.levels.insert(0, l)
            play()
