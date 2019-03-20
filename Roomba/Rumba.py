# -*- coding: utf-8 -*-
""" Robot Vacuum Cleaner """

from collections import deque
import random

import os
if os.sys.version_info.major > 2: 
    xrange = range
    import tkinter as tk
else:
    import Tkinter as tk

#### METHODS ####

def scale_vector(vector, velocity):
    """
    Create unit vector. Multiply each component of unit vector
    by the magnitude of the desired vector (velocity).
    """
    try:
        x = float(vector[0])/((vector[0]**2+vector[1]**2)**.5)
        y = float(vector[1])/((vector[0]**2+vector[1]**2)**.5)
        return int(x*velocity), int(y*velocity)
    except ZeroDivisionError:
        return None, None
    
def get_random_velocity(velocity):
    """
    Create random direction vector.
    Scale direction vector with scale_vector method.
    """
    vx, vy = None, None
    while vx == None and vy == None:
        vector = (random.random()*random.choice([-1, 1]),
                 random.random()*random.choice([-1, 1]))
        vx, vy = scale_vector(vector, velocity)
    return vx, vy

def make_grid(furniture, dimension):
    """
    Scale actual (x, y) positions down to a grid (dictionary) 
    with keys (Nx*1, Ny*1) where Nx and Ny range from 1 to dimension[0] 
    and 1 to dimension[1] respectively.
    The keys are mapped to a boolean indicating whether that tile
    is occupied with furniture (True) or not (False).
    furniture: list with pixle locations. Each element ~ (x, y, x+dx, y+dy).
    dimension: tuple, x by y dimensions (x, y).
    returns: grid = {(1, 1): False, (2, 1): True, ...}
    """
    #dx, dy are width and height of tiles.
    dx = furniture[0][2] - furniture[0][0]
    dy = furniture[0][3] - furniture[0][1]
    w, h = dx*dimension[0], dy*dimension[1]
    
    grid = {}
    for y in xrange(1, dimension[1]+1):
        for x in xrange(1, dimension[0]+1):
            grid[(x, y)] = False
    
    y_grid = 0
    for y in xrange(dy//2, h, dy):
        y_grid += 1
        x_grid = 0
        for x in xrange(dx//2, w, dx):
            x_grid += 1
            for element in furniture:
                if x >= element[0] and x <= element[2] \
                and y >= element[1] and y <= element[3]:
                    grid[(x_grid, y_grid)] = True
                    break
    return grid
    
def get_neighbors(position):
    """
    Generator. Yields positions to the left, to the right,
    above, and below the current position.
    """
    deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for d in deltas:
        yield position[0]+d[0], position[1]+d[1]
    
#def find_accessable_tiles_RECURSIVE(grid, position, l=set()):
#    """
#    Finds all non-furniture locations that are accessable
#    when starting at position 'position'.
#    *** Mutates l ***
#    Assumes position is not at a point such that grid[position] == True.
#    In other words, the initial positions is valid and is not occupied.
#    grid: dict mapping a Grid to booleans (tiles with/without furniture).
#        i.e. grid = {(1, 1): False, (2, 1): True, ...}
#    position: tuple (x, y)
#    l: list
#    """
#    l.add(position)
#    for n in get_neighbors(position):
#        if n in grid and n not in l and not grid[n]:
#            find_accessable_tiles(grid, n, l)
#    return l

def find_accessable_tiles(grid, position):
    """
    Finds all tiles that are accessable from starting position.
    Returns a set of all accessable tiles.
    """
    accessable = set()
    accessable.add(position)
    tile_queue = deque() #imported from collections
    tile_queue.append(position)
    while tile_queue:
        current = tile_queue.popleft()
        for n in get_neighbors(current):
            if n in grid and n not in accessable and not grid[n]:
                accessable.add(n)
                tile_queue.append(n)
    return accessable
    
def is_furniture_valid(furniture, dimension):
    """
    Checks to see if all non-furniture tiles can be accessed
    when starting initially at position (1, 1).
    furniture: list of (x, y, x+dx, y+dy).
    dimension: tuple, x by y dimensions (x, y).
    """
    if not furniture: #Rooms with no furniture are valid.
        return True
    grid = make_grid(furniture, dimension)
    #Start position is (1, 1).
    accessable_tiles = find_accessable_tiles(grid, (1, 1))
    #Compare accessable tiles to all non-furniture tiles.
    for element in grid:
        #if a tile doesn't have furniture AND is not accessible - not valid.
        if not grid[element] and element not in accessable_tiles:
            return False
    return True

#### OBJECT DEFINITIONS ####
    
class Rumba(object):
    """
    Dealing with the actual Rumba robot on the screen - red square.
    canvas: tk.Canvas object.
    position: tuple (x, y).
    width: int width of square.
    """
    def __init__(self, canvas, position, width):       
        self.can, self.width = canvas, width  
        self.Draw(position)
        
    def Draw(self, position):
        x, y = position
        x1, y1 = x + self.width, y + self.width
        x2, y2 = x + self.width, y - self.width
        x3, y3 = x - self.width, y - self.width
        x4, y4 = x - self.width, y + self.width
        
        self.vacuum = self.can.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, fill="red")
        self.line1 = self.can.create_line(x1, y1, x2, y2, fill="black")
        self.line2 = self.can.create_line(x2, y2, x3, y3, fill="black")
        self.line3 = self.can.create_line(x3, y3, x4, y4, fill="black")
        self.line4 = self.can.create_line(x1, y1, x4, y4, fill="black")
        
    def update_position(self, new_position):
        x, y = new_position       
        x1, y1 = x + self.width, y + self.width
        x2, y2 = x + self.width, y - self.width
        x3, y3 = x - self.width, y - self.width
        x4, y4 = x - self.width, y + self.width
        
        self.can.coords(self.vacuum, x1, y1, x2, y2, x3, y3, x4, y4)
        self.can.coords(self.line1, x1, y1, x2, y2)
        self.can.coords(self.line2, x2, y2, x3, y3)
        self.can.coords(self.line3, x3, y3, x4, y4)
        self.can.coords(self.line4, x1, y1, x4, y4)
        
class Grid(object):
    """
    The grid that the vacuum will clean.
    canvas: tk.Canvas object.
    dimension: tuple of number of tiles (x, y).
    screen: tuple of size of canvas (w, h).
    furniture: boolean - if room will have furniture.
    """
    def __init__(self, canvas, dimension, screen, furniture=True):
        self.can, self.dimension = canvas, dimension
        self.w, self.h = screen
        
        self.create_tiles(furniture)
        
    def create_tiles(self, furniture):
        """
        Finds a valid configuration of furniture and tiles.
        Then, calls self.draw_tiles to draw configuration.
        """
        #dx, dy are width and height of tiles.
        dx, dy = self.w//self.dimension[0], self.h//self.dimension[1]
        
        #adjust screen size for discrepincies in forcing int divition.
        self.w, self.h = self.dimension[0]*dx, self.dimension[1]*dy
        self.can.config(width=self.w, height=self.h)
        
        valid = False
        while not valid:
            tiles, furniture_tiles = [], []
            for y in xrange(0, self.h, dy):
                for x in xrange(0, self.w, dx):
                    #(0, 0) is always a non-furniture tile.
                    if not furniture or random.random() <= 0.8 or (x, y) == (0, 0):                    
                        tiles.append((x, y, x+dx, y+dy))
                    else:
                        furniture_tiles.append((x, y, x+dx, y+dy))
            valid = is_furniture_valid(furniture_tiles, self.dimension)
            
        self.draw_tiles(tiles, furniture_tiles)
    
    def draw_tiles(self, tiles, furniture_tiles):
        """
        Draws a configuration of furniture and tiles.
        tiles: list of position tuples, (x, y, x+dx, y+dy).
        furniture_tiles: same as tiles but only for furniture.
        """
        self.furniture = furniture_tiles
        for element in self.furniture:
            x, y = element[0], element[1]
            dx, dy = element[2] - x, element[3] - y
            self.can.create_rectangle(x, y, x+dx, y+dy, fill="green")
        
        self.tiles = {}
        for element in tiles:
            x, y = element[0], element[1]
            dx, dy = element[2] - x, element[3] - y
            self.tiles[element] = [4,  
                    self.can.create_rectangle(x, y, x+dx, y+dy, fill="black")]
                        
    def get_tile(self, position):
        x, y = position
        for element in self.tiles:
            if (x >= element[0] and x <= element[2] 
            and y >= element[1] and y <= element[3]):
                return element
                
    def clean_tile(self, position):
        """
        Takes 4 times to clean a tile.
        Usually, vacuum will clean 2 at a time though.
        *** On some screens, 'dark grey' is lighter than 'grey'. ***
        """
        tile = self.get_tile(position)
        self.tiles[tile][0] -= 1
        if self.tiles[tile][0] == 0:
            self.can.itemconfig(self.tiles[tile][1], fill="white")
        elif self.tiles[tile][0] == 1:
            self.can.itemconfig(self.tiles[tile][1], fill="light grey")
        elif self.tiles[tile][0] == 2:
            self.can.itemconfig(self.tiles[tile][1], fill="grey")
        elif self.tiles[tile][0] == 3:
            self.can.itemconfig(self.tiles[tile][1], fill="dark grey")
            
    def is_grid_cleaned(self):
        for element in self.tiles.values():
            if element[0] > 0:
                return False
        return True
            
    def get_dimension(self):
        return self.dimension
    def get_grid_size(self):
        return (self.w, self.h)
    def get_furniture(self):
        return self.furniture
        
class Robot(object):
    """
    Completes the numerical simulation.
    grid: a Grid object.
    canvas: a tk.Canvas object.
    v: int speed of robot.
    """
    def __init__(self, grid, canvas, v):
        self.grid = grid
        self.w, self.h = self.grid.get_grid_size()
        self.furniture = self.grid.get_furniture()
        
        self.v = v
        self.set_random_velocity()
        
        average_size = sum(self.grid.get_grid_size())/2
        average_dimension = sum(self.grid.get_dimension())/2
        self.robot_width = int((average_size/average_dimension)*0.3)
        #initial position
        self.x, self.y = self.robot_width, self.robot_width
        
        self.rumba = Rumba(canvas, (self.x, self.y), self.robot_width)
            
    def is_valid_position(self, position):
        x, y = position
        if x + self.robot_width >= self.w or x - self.robot_width <= 0:
            return False
        elif y + self.robot_width >= self.h or y - self.robot_width <= 0:
            return False
        for element in self.furniture:
            #element is of the form (x, y, x+dx, y+dy)
            if x >= element[0] and x <= element[2]:
                if y >= element[1] and y <= element[3]:
                    return False
                elif y + self.robot_width >= element[1] and y + self.robot_width <= element[3]:
                    return False
                elif y - self.robot_width >= element[1] and y - self.robot_width <= element[3]:
                    return False
            elif x + self.robot_width >= element[0] and x + self.robot_width <= element[2]:
                if y >= element[1] and y <= element[3]:
                    return False
                elif y + self.robot_width >= element[1] and y + self.robot_width <= element[3]:
                    return False
                elif y - self.robot_width >= element[1] and y - self.robot_width <= element[3]:
                    return False
            elif x - self.robot_width >= element[0] and x - self.robot_width <= element[2]:
                if y >= element[1] and y <= element[3]:
                    return False
                elif y + self.robot_width >= element[1] and y + self.robot_width <= element[3]:
                    return False
                elif y - self.robot_width >= element[1] and y - self.robot_width <= element[3]:
                    return False       
        return True        
    
    def set_random_velocity(self):
        self.vx, self.vy = get_random_velocity(self.v)
            
    def update(self):
        """
        Checks to see if current direction is valid.
        If it is, continues, if not, picks new,
        random directions until it finds a valid direction.
        """
        x, y = self.x+self.vx, self.y+self.vy
        while (x, y) == (self.x, self.y) or not self.is_valid_position((x, y)):
            self.set_random_velocity()
            x, y = self.x+self.vx, self.y+self.vy
        self.x, self.y = x, y
        self.rumba.update_position((self.x, self.y))
        self.grid.clean_tile((self.x, self.y))
        
#### OBJECTS MANAGER ####
        
class Home(object):
    """
    Manages Simulation.
    master: tk.Tk object.
    screen: tuple (width, height).
    dimension: tuple, dimension of the grid.
    """
    def __init__(self, master, screen, dimension):        
        frame = tk.Frame(master)
        frame.pack()
               
        v = sum(screen)//(2*sum(dimension))

        canvas = tk.Canvas(frame, width=screen[0], height=screen[1])
        canvas.pack()
        grid = Grid(canvas, dimension, screen)
        robot = Robot(grid, canvas, v)
        
        master.title("Roomba Robot - Steps: 0")
        master.bind('<Return>', self.restart)
        master.bind('<Up>', self.fast)
        master.bind('<Down>', self.slow)
        
        #initialize class variables.
        self.master, self.frame = master, frame
        self.screen, self.dimension = screen, dimension
        self.robot, self.grid = robot, grid
        
        #self.speed adjusts frame rate. Can be manipulated with arrow keys.
        #self.count keeps track of steps.
        self.speed, self.count = 100, 0
        
        self.update()
        
    def restart(self, callback=False):
        """ Enter/Return Key """
        self.frame.destroy()
        self.__init__(self.master, self.screen, self.dimension)
        
    def fast(self, callback=False):
        """ Up arrow key """
        if self.speed > 5:
            self.speed -= 5
        else:
            self.speed = 1
    
    def slow(self, callback=False):
        """ Down arrow key """
        self.speed += 5
        
    def update(self):
        self.robot.update()
        self.count += 1
        self.master.title("Rumba Robot - Steps: %d" % self.count)
        
        if not self.grid.is_grid_cleaned():
            self.frame.after(self.speed, self.update)
        else:
            self.frame.bell()
            
#### SIMULATION ####
            
def simulate(screen, dimension):
    """ 
    screen: tuple, screen size in pixles: (width, height).
    dimension: tuple, dimension of grid: (x, y).
    """
    root = tk.Tk()
    root.resizable(0, 0)
    try: root.wm_iconbitmap("ploticon.ico")
    except: pass
    
    Home(root, screen, dimension)
    #Center window on screen.
    #root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    root.mainloop()
        
if __name__ == "__main__":
    """   
    Tip: Up/Down arrow keys will speed/slow the simulation.
    Enter/Return will restart with the same screen and dimension attributes.
    
    *** Large dimensions may take a few minutes to generate ***
    """
    screen = 1000, 700
    dimension = 30, 20
    
    simulate(screen, dimension)