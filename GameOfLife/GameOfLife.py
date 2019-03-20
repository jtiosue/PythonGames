# -*- coding: utf-8 -*-
"""
Conway's Game of Life.

Note: this version does NOT assume an infinite grid.
(In my opinion, a finite area is more relatable to "life").

Up/Down arrow keys speed/slow the simulation.
Spacebar starts the simulation.
Enter/Return resets the screen.
Draw live cells with left-click mouse drag.
Erase live cells with right-click mouse drag.
"""

### Game rules ###
MAX_NEIGHBORS = 3   ## More neighbors than this kills a live cell.
MIN_NEIGHBORS = 2   ## Less neighbors than this kills a live cell.
IDEAL_NEIGHBORS = 3 ## This many neighbors around dead cell creates live cell.

### Settings ###
DIMENSION = 75, 40 #Tile dimension size (x, y).
LIVE_COLOR, DEAD_COLOR = "green", "white"

## Account for edge effects on canvas.
ZERO = 2

#############################################################################

## Maintain compatability between Python versions while still
## raising ImportError if tk module is not installed.
try:
    xrange
    import Tkinter as tk
except NameError:
    xrange = range
    import tkinter as tk


def get_neighbors(position):
    """ 
    Generator that yields position tuples of neighbors (including diagonals).
    position: tuple (x, y).
    """
    for x in xrange(-1, 2):
        for y in xrange(-1, 2):
            if x or y: #(0, 0) is not a neighbor.
                yield position[0] + x, position[1] + y
    # yield from filter(lambda t: t[0] or t[1], ((x, y) for x in xrange(-1, 2) 
                                                      # for y in xrange(-1, 2)))

class Grid(tk.Canvas):
    """
    Deals with screen animation and game simulation.
    SubClass of tk.Canvas. Can be packed onto tk.Tk or tk.Frame.
    
    frame: tk.Frame to pack canvas on.
    dimension: tuple, tile dimension (x, y).
    screen: tuple, screen size (width, height).
    """
    def __init__(self, frame, dimension, screen):
        tk.Canvas.__init__(self, frame)
        #Adjust screen size for discrepencies from forced int division.
        dx, dy = screen[0]//dimension[0], screen[1]//dimension[1]
        #Doesn't work well with tiles smaller than 4 pixles in width or height.
        assert dx > 3 and dy > 3, "Dimension to screen ratio is too small."
        w, h = dx*dimension[0], dy*dimension[1]
        self.config(width=w+ZERO, height=h+ZERO)
    
        self.tiles  = {}
        y_grid = 0
        for y in xrange(ZERO, h+ZERO, dy):
            x_grid = 0
            y_grid += 1
            for x in xrange(ZERO, w+ZERO, dx):
                x_grid += 1
                args = (x, y, x+dx, y+dy)
                self.tiles[(x_grid, y_grid)] = [
                               args,
                               self.create_rectangle(*args, fill=DEAD_COLOR),
                               False  #Boolean for if cell is live. Start dead.
                ]

    def get_tile(self, position):
        """
        Returns tuple (x, y) if position is valid:
            i.e. the key to the tile in self.tiles at the specified position.
        If position is invalid, returns None.
            
        position: tuple, pixel location on screen (x, y).
        """
        x, y = position
        for tile in self.tiles:
            rect_def = self.tiles[tile][0]
            if (x >= rect_def[0] and x <= rect_def[2]
            and y >= rect_def[1] and y <= rect_def[3]):
                return tile
                
    def is_tile_live(self, tile):
        """ 
        Returns boolean: True if tile is live, else False. 
        tile: tuple (x, y), key of tile in self.tiles.        
        """
        return tile in self.tiles and self.tiles[tile][2]
                
    def make_live(self, tile):
        """
        Make specified tile live.
        tile: tuple (x, y), key of tile in self.tiles. 
        """
        self.itemconfig(self.tiles[tile][1], fill=LIVE_COLOR)
        self.tiles[tile][2] = True
        
    def make_dead(self, tile):
        """
        Make specified tile dead.
        tile: tuple (x, y), key of tile in self.tiles. 
        """
        self.itemconfig(self.tiles[tile][1], fill=DEAD_COLOR)
        self.tiles[tile][2] = False
        
    def num_live_neighbors(self, tile):
        """
        Returns int, number of live neighbors the specified tile has.
        tile: tuple (x, y), key of tile in self.tiles. 
        """
        total = 0
        for n in get_neighbors(tile):
            if self.is_tile_live(n):
                total += 1
        return total
        
    def all_dead(self):
        """ Return boolean: True if all tiles are dead, else False. """
        ## Using 'any' should be faster than 'all' for most cases.
        ## i.e. return all(not self.is_tile_live for tile in self.tiles)
        ## will ALWAYS loop through all of self.tiles, as opposed to the
        ## below implementation of 'any' which will usually not have
        ## to loop through the entire key set of self.tiles.
        return not any(self.is_tile_live(tile) for tile in self.tiles)
        
    def update(self):
        """
        Implements game rules using current grid configuration.
        IMPORTANT: updates canvas AFTER ALL tiles have been updated.
        """
        to_make_dead, to_make_live = [], []
        for tile in self.tiles:
            num_live = self.num_live_neighbors(tile)
            if self.is_tile_live(tile):
                if num_live < MIN_NEIGHBORS or num_live > MAX_NEIGHBORS:
                    to_make_dead.append(tile)
            else:
                if num_live == IDEAL_NEIGHBORS:
                    to_make_live.append(tile)
                    
        for tile in to_make_live:
            self.make_live(tile)
        for tile in to_make_dead:
            self.make_dead(tile)
    

class Home(tk.Frame):
    """
    Subclass of tk.Frame. Can be packed on tk.Tk window.
    master: tk.Tk window.
    """
    SPEED = 500 #Milliseconds between screen redraw.
    def __init__(self, master):
        master.title("Conway's Game of Life")
        #User can resize the screen size as desired.
        master.update()
        screen = master.winfo_width(), master.winfo_height()
        
        tk.Frame.__init__(self, master)  
        #Initialize grid (tk.Canvas object). Pack it onto frame (self).
        self.grid = Grid(self, DIMENSION, screen)
        self.grid.pack()
        
        self.playing, self.count = False, 0
        #Initialize instance variable.
        self.master = master
        
    def increase_fps(self):
        """ Decreases milliseconds between screen redraw. """
        if Home.SPEED > 5:
            Home.SPEED -= 5
        else:
            Home.SPEED = 1
            self.bell()
    
    def decrease_fps(self):
        """ Increases milliseconds between screen redraw. """
        Home.SPEED += 5
        
    def draw(self, position):
        """
        Make tile at position live.
        position: tuple, pixel location (x, y).
        """
        #If position is off screen, tile will equal None.
        tile = self.grid.get_tile(position)
        if tile:
            self.grid.make_live(tile)
    
    def erase(self, position):
        """
        Make tile at position dead.
        position: tuple, pixel location (x, y).
        """
        #If position is off screen, tile will equal None.
        tile = self.grid.get_tile(position)
        if tile:
            self.grid.make_dead(tile)
    
    def restart(self):
        """ Destroy current frame, reinitialize class, repack frame. """
        self.destroy()
        self.__init__(self.master)
        self.pack()
        
    def update(self):
        """ Update counter and grid. Recall after self.speed milliseconds. """
        self.count += 1
        self.master.title("Steps: %d" % self.count)
        self.grid.update()
        
        if not self.grid.all_dead():
            self.after(Home.SPEED, self.update)
        
    def start(self):
        """ Begin simulation. """
        if not self.playing:
            self.update()
            self.playing = True
            
        
def main():
    """
    Open main window, pack Home frame, bind key controls.
    """
    root = tk.Tk()
    root.state("zoomed") #Begin with window maximized.
    home = Home(root) #Subclass of tk.Frame.
    home.pack() #Pack onto window.
    
    #Key bindings.
    root.bind("<Return>", lambda event: home.restart())
    root.bind("<Up>", lambda event: home.increase_fps())
    root.bind("<Down>", lambda event: home.decrease_fps())
    root.bind("<B1-Motion>", lambda event: home.draw((event.x, event.y)))
    root.bind("<B3-Motion>", lambda event: home.erase((event.x, event.y)))
    root.bind("<space>", lambda event: home.start())
    root.bind("<Escape>", lambda event: root.destroy())
    
    root.mainloop()
    

if __name__ == "__main__":
    main()