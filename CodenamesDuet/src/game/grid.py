import random

## num greens to have on each side
_NUM_GREENS = 9

## sum of num of greens on both sides
TOTAL_NUM_GREENS = 15


class _Player_Grid:
    
    def __init__(self, colors):
        """ colors is a length 25 list of "t", "g", and "b" """
        if len(colors) != 25:
            raise ValueError("Grid must be 5x5")
        self._colors = colors
            
        
    def _get_index(self, row, col):
        if row not in range(5) or col not in range(5):
            raise ValueError("Row or Column out of range")
        return 5*row + col
    
    def get_color(self, row, col):
        return self._colors[self._get_index(row, col)]
    
    def get_colors(self):
        return self._colors
    
    def invert(self):
        """ invert the display """
        new_colors = [""]*25
        for r in range(5):
            for c in range(5):
                new_colors[self._get_index(4-r, 4-c)] = self.get_color(r, c)
        return _Player_Grid(new_colors)
    
    def __getitem__(self, index):
        return self._colors[index]      

    def __str__(self):
        s = ""
        for r in range(5):
            for c in range(5):
                s += self.get_color(r, c) + "  "
            s += "\n"
        return s    
    
    
def _init_rand_grid():
    l = ["b"]*3 + ["g"]*_NUM_GREENS + ["t"]*(22-_NUM_GREENS)
    random.shuffle(l)
    return _Player_Grid(l)


def _match_grid(grid):
    """
    given a grid, create the other side to obey:
        one p1 black must be a p2 green, tan, and black; and vice versa
    """
    l = [""] * 25
    
    color_dict = {
        "b": [i for i in range(25) if grid[i] == "b"],
        "t": [i for i in range(25) if grid[i] == "t"],
        "g": [i for i in range(25) if grid[i] == "g"]
    }
    
    random.shuffle(color_dict["b"])
    
    l[color_dict["b"][0]] = "b"
    l[color_dict["b"][1]] = "g"
    l[color_dict["b"][2]] = "t"
    
    x = random.choice(color_dict["g"])
    color_dict["g"].remove(x)
    l[x] = "b"
    l[random.choice(color_dict["t"])] = "b"
    
    
    # one green is the other player's black 
    # three are the other players greens
    remain = {i for i in range(25) if l[i] == ""}
    
    s = random.sample(remain.difference(set(color_dict["g"])), _NUM_GREENS - 4)
    s += random.sample(color_dict["g"], 3)
    
    for i in remain:
        if i in s: l[i] = "g"
        else: l[i] = "t"
    
    return _Player_Grid(l)

    
class Grid:
    
    def __init__(self):
        self._p1_color = _init_rand_grid()
        self._p2_color = _match_grid(self._p1_color)
        
    def get_p1_color(self, row, col):
        return self._p1_color.get_color(row, col)
    
    def get_p2_color(self, row, col):
        return self._p2_color.get_color(row, col)
    
    def get_color(self, row, col, player):
        if player == 1: return self.get_p1_color(row, col)
        else: return self.get_p2_color(row, col)
    
    def display_p1(self):
        return self._p1_color.get_colors()
    
    def display_p2(self):
        # maybe invert
        # but probably not because will be on different screens anyways
        return self._p2_color.get_colors()