# -*- coding: utf-8 -*-
""" Rocket Ace - Maneuver a rocket in space around obstacles. """

#### GLOBAL VARIABLES ####

## Most widths and heights are in universal scale vw, vh (i.e. out of 100).
## They are scaled later in accordance with the screen size.
## For example, coordinate (15, 20) on a screen size (500, 300) corresponds
## to (75, 60) in pixles.

HELPFILE = "help.txt"

#Adjust controls.
GAME_CONTROLS = LEFT, RIGHT, UP, DOWN = "Left", "Right", "Up", "Down"
RESTART, EXIT = "Return", "Escape"

#Kinds of obstacles.
KINDS = OVAL, LINE, POLYGON, ARC, RECTANGLE, START, END = (
    "oval", "line", "polygon", "arc", "rectangle", "start", "end"
)
ORDERING = "KIND, COLOR, X0, Y0, X1, Y1, ..."

PLAYER_WIDTH, PLAYER_COLOR = 2, "red"

BLACK, WHITE = "black", "white"
FONTSTYLE = "ms %d" #%d is for fontsize.
FONT = FONTSTYLE % 12
TEXT = "ROCKET ACE    Level %s    %s: %d seconds" #%s is one of the three below.
COMPLETE, FAIL, ELAPSED = "Completed", "Failed", "Elapsed Time"

SPEED = 20 #milliseconds between screen redraw.
SCALE_A = 200.0 #Adjust arbitrary acceleration scale values to meaninful values.
MAX_A = 10.0 #Maximum acceleration value to appear on scale.

CUSHION = 0.4 #before scaling. Gives leniancy to player.
ZERO = 2 #in pixels. Prevents left and top edge widgets from getting cut off.

###############################################################################

import time, os

if os.sys.version_info.major > 2:
    xrange = range
    import tkinter as tk
else:
    import Tkinter as tk

#### Error Types and Error Methods ####

class EndpointError(Exception):
    """ All level files must include both start and end points """
    
class KindError(Exception):
    """ Kind of obstacle must be in KINDS """
    
class ArgumentError(Exception):
    """ Error for invalid arguments for obstacles """

def is_valid(f):
    """
    f: open file for reading.
    returns None.
    If file is not valid for a level, raises an exception.
    """
    line_num = 0
    start, end = False, False
    for line in f:
        line_num += 1
        if line.strip() and line.strip()[0] != "#":
            l = line.split(",")
            if len(l) < 6:
                raise ArgumentError(
                            "line %d: Must have at least 6 arguments ordered %s" 
                            % (line_num, ORDERING)
                )
            kind = l[0].strip().lower()
            if kind not in KINDS:
                raise KindError("line %d: Got '%s', expected kind in %s"
                                % (line_num, kind, KINDS)
                )
            try: args = [float(x.strip()) for x in l[2:]]
            except:
                raise ArgumentError(
                "line %d: Line must be ordered %s. Coordinates must be numbers." 
                % (line_num, ORDERING)
                )
            if len(args) % 2:
                raise ArgumentError(
                                "line %d: Must have pairs of coordinates (x, y)"
                                % line_num
                )
            if kind != POLYGON and kind != LINE and len(args) > 4:
                raise ArgumentError(
                        "line %d: %s should only have 4 coordinates (2 pairs)." 
                        % (line_num, kind)
                )
            if kind == START: start = True
            elif kind == END: end = True            
    if not start or not end:
        if not start and not end:
            missing = "%s and %s" % (START.upper(), END.upper())
        else: 
            missing = START.upper() if not start else END.upper()
        raise EndpointError("%s missing. Expected two endpoints" % missing)
        
def display_error(name, message):
    """
    name: str, type of error to display as title.
    message: str, error message to display.
    
    Create new window, display error message.
    """
    root = tk.Tk()
    root.resizable(0, 0)
    root.bell()
    color = "#ffe6e6"
    root.config(bg=color)
    root.title(name)
    root.attributes("-toolwindow", 1)
    tk.Label(root, text=message, bg=color).pack()
    tk.Button(root, text="Okay", command=root.destroy, width=7).pack()
    root.eval('tk::PlaceWindow %s center'%root.winfo_pathname(root.winfo_id()))
    root.bind("<Return>", lambda event: root.destroy())
    root.mainloop()

#### METHODS ####

def avg(l):
    """
    Returns average of list or tuple.
    l: list or tuple.
    """
    return float(sum(l))/float(len(l))
    
def scaling_factor(screen):
    """
    Create universal scale for all screens based
    around a max width and height of 100.
    screen: tuple, screen size (w, h).
    """
    return screen[0]/100.0, screen[1]/100.0    
    
def apply_cushion(x0, x1, cushion):
    """
    x0, x1: ints, x coordinates of corners.
    cushion: float, how much leniancy to give.
    """
    if x0 < x1:
        x0 += cushion
        x1 -= cushion
    else:
        x0 -= cushion
        x1 += cushion
    return x0, x1
    
def get_levels():
    """
	returns a list of all levels sorted.
	defined in directory /levels/.
	"""
    level_num, level_alp = [], []
    for f in os.listdir("levels"):
        if f[:5] == "level":
            try:
                level_num.append(int(f.split(".")[0][5:]))
            except ValueError:
                level_alp.append(f.split(".")[0][5:])
    level_num.sort()
    level_alp.sort()
    return level_num + level_alp

#### OBJECT DEFINITIONS ####        
    
class Obstacle(object):
    """
    kind: str, must be in KINDS.
    color: str, color of obstacle.
    args: list, coordinates [x0, y0, x1, y1, ...].
    """
    LINE_WIDTH = 0.5 #Also used as argument for font size for endpoints.
    def __init__(self, kind, color, args):
        self.args = args
        self.kind, self.color, self.w = kind, color, Obstacle.LINE_WIDTH
        
    def scale_coords(self, screen):
        """ 
        Create universal scale for all screens. 
        screen: tuple, screen size (w, h).
        """
        x_scale, y_scale = scaling_factor(screen)
        
        for i in xrange(len(self.args)):
            if i % 2: self.args[i] *= y_scale #odd indices are y coordinates.
            else: self.args[i] *= x_scale #even index are x coordinates.
        
        self.w *= avg((x_scale, y_scale)) #scale line width.
        
    def create_object(self, canvas):
        """
        returns tk.Canvas.create_[kind] object.
        canvas: tk.Canvas object to draw on.
        """
        if self.kind == RECTANGLE:
            return canvas.create_rectangle(*self.args, fill=self.color)
        elif self.kind == OVAL:
            return canvas.create_oval(*self.args, fill=self.color)
        elif self.kind == POLYGON:
            return canvas.create_polygon(*self.args, fill=self.color)
        elif self.kind == ARC:
            return canvas.create_arc(*self.args, fill=self.color)
        elif self.kind == LINE:
            return canvas.create_line(*self.args, width=self.w, fill=self.color)

                                       
class Endpoints(Obstacle):
    """
    A rectangular instance of Obstacle with text added.
    pt: str, either START or FINISH.
    color: str, color of obstacle.
    args: list, coordinates [x0, y0, x1, y1, ...].
    """
    FONT = FONTSTYLE
    def __init__(self, pt, color, args):
        Obstacle.__init__(self, RECTANGLE, color, args)
        self.pt = pt.upper()
    
    def create_object(self, canvas):
        ob = Obstacle.create_object(self, canvas)
        #middle of object WITH scaled coordinates.
        self.x = avg([self.args[i] for i in xrange(0, len(self.args), 2)])
        self.y = avg([self.args[i] for i in xrange(1, len(self.args), 2)])
        canvas.create_text(self.x, self.y, text=self.pt, 
                           font=Endpoints.FONT % (self.w*5))
        return ob
       
       
class Start(Endpoints):
    """
    color: str, color of obstacle.
    args: list, coordinates [x0, y0, x1, y1, ...].
    """
    def __init__(self, color, args):
        Endpoints.__init__(self, START, color, args)
        
    def get_middle_coords(self):
        """ Returns middle of rectangle WITH scaled coordinates. """
        return self.x, self.y


class End(Endpoints):
    """
    color: str, color of obstacle.
    args: list, coordinates [x0, y0, x1, y1, ...].
    """
    def __init__(self, color, args):
        Endpoints.__init__(self, END, color, args)

  
class File(object):
    """ 
    Methods for Files.
    filename: str, name of file to read from.
    """
    def __init__(self, filename):
        with open(filename, "r") as f:
            is_valid(f) #Raises exception if there are any errors.
            
        #Read file and create Obstacle, Start, and End objects from it.
        self.obstacles = []
        with open(filename, "r") as f:
            for line in f:
                #ignore empty lines or commented lines.
                if line.strip() and line.strip()[0] != "#":
                    #line is formated as 'kind, color, *args'.
                    l = line.split(",")
                    kind, color = l[0].strip().lower(), l[1].strip().lower()
                    args = [float(x.strip()) for x in l[2:]]
                    if kind == START:
                        self.start = Start(color, args)
                    elif kind == END:
                        self.end = End(color, args)
                    else:
                        self.obstacles.append(Obstacle(kind, color, args))
            
    def get_obstacles(self):
        return self.obstacles
    def get_endpoints(self):
        return self.start, self.end


class Background(object):
    """
    filename: str, name of file to read from.
    canvas: tk.Canvas object to draw on.
    screen: tuple, screen size (w, h).
    """
    def __init__(self, filename, canvas, screen):
        canvas.config(bg=BLACK, width=screen[0], height=screen[1])
        
        f = File(filename)
        
        #Create Endpoints. 
        #self.start_coords will be tuple of coords (x, y).
        #self.end will be tk.Canvas.create_rectangle object.
        start, end = f.get_endpoints()
        start.scale_coords(screen)
        start.create_object(canvas)
        self.start_coords = start.get_middle_coords()
        end.scale_coords(screen)
        self.end = end.create_object(canvas)
        
        #Create Obstacles.
        self.obstacles = []
        for element in f.get_obstacles():
            element.scale_coords(screen)
            self.obstacles.append(element.create_object(canvas))
        
        #adjust to give leniancy to player (i.e. around corners).
        self.xcushion, self.ycushion = scaling_factor(screen)
        self.xcushion *= CUSHION
        self.ycushion *= CUSHION
        
        self.can, self.screen = canvas, screen
        
    def is_position_valid(self, x0, y0, x1, y1):
        """ 
        x0, y0, x1, y1: ints, coords that define players position. 
        returns END if position is at end point.
        Othewise, returns True or False.
        """
        #Give leniancy to player.         
        x0, x1 = apply_cushion(x0, x1, self.xcushion)
        y0, y1 = apply_cushion(y0, y1, self.ycushion)
            
        if (x0 < 0 or x1 < 0 or x0 > self.screen[0] or x1 > self.screen[0] or
            y0 < 0 or y1 < 0 or y0 > self.screen[1] or y1 > self.screen[1]):
            return False
            
        overlapping = self.can.find_overlapping(x0, y0, x1, y1)
        if self.end in overlapping: return END
        else: return not any(ob in overlapping for ob in self.obstacles)

    def get_start_coords(self):
        """ returns middle coordinates of start position. """
        return self.start_coords
 
       
class OnScreenPlayer(object):
    """
    On Screen manager of player: 
    canvas: tk.Canvas object to draw on.
    position: tuple, initial position (x, y).
    width: int.
    """
    SMOKE = True #White line trailing rocket.
    def __init__(self, canvas, position, width):
        self.can, self.w = canvas, width
        
        x, y = position
        self.player = self.can.create_oval(x-self.w, y-self.w, x+self.w, 
                                           y+self.w, fill=PLAYER_COLOR)                                        
        self.x, self.y = position #old coordinates. Used for smoke.
        
    def update_position(self, position):
        """
        Updates position on screen.
        If OnScreenPlayer.SMOKE, draws a white line from old position to new.
        """
        x, y = position
        self.can.coords(self.player, x-self.w, y-self.w, x+self.w, y+self.w)        

        if OnScreenPlayer.SMOKE:
            self.can.create_line(self.x, self.y, x, y, 
                                 fill=WHITE, width=self.w/3)
        #reset old coordinates. Used for smoke.
        self.x, self.y = position

        
class Player(object):
    """
    canvas: tk.Canvas object to draw on.
    background: Background object with obstacles.
    width: int.
    """
    def __init__(self, canvas, background, width):
        self.background, self.w = background, width
        
        self.x, self.y = self.background.get_start_coords()
        self.player = OnScreenPlayer(canvas, (self.x, self.y), self.w)
        
        self.vx, self.vy = 0, 0 #initially at rest.

    def update(self, ax, ay):
        """ 
        Update speed and position with given acceleration values.
        Then, update position on screen.
        ax, ay: floats.
        """
        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy
        self.player.update_position((self.x, self.y))
        
    def is_position_valid(self):
        """ returns END if player has reached the end; else True or False """
        x0, y0 = self.x-self.w, self.y-self.w
        x1, y1 = self.x+self.w, self.y+self.w
        return self.background.is_position_valid(x0, y0, x1, y1)
      
    
class Level(object):
    """
    master: tk.Tk window.
    screen: tuple, screen size (w, h).
    level: int, level number.
    """
    STEP = 0.5 #For how quickly scales inc/dec with arrow keys.
    def __init__(self, master, screen, level="0"):
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.can = tk.Canvas(self.frame)
        self.can.pack()
        
        master.title("Rocket Ace: Level %s" % level)
        
        #Create background and player.
        filename = "levels/level%s.txt" % level
        background = Background(filename, self.can, screen)
        
        #Use min to ensure that player isn't too big for certain screen sizes.
        w = PLAYER_WIDTH * min(scaling_factor(screen))
        self.user = Player(self.can, background, w)
        
        #Label to display time elapsed.
        self.label = tk.Label(self.frame, font=FONT, pady=10)
        self.label.pack()
        
        #These are true when arrow keys are pressed, false when not.
        self.up, self.down, self.left, self.right = False, False, False, False
        
        self.master, self.level, self.screen = master, level, screen
        
        self.create_acceleration_scales()
        
    def create_acceleration_scales(self):
        l, w = 75, 15
        kwargs = {"bg": BLACK, "fg": WHITE, "resolution": 0.1, "length": l, 
                  "width": w, "borderwidth": 0, "highlightthickness": 0}
        
        self.ax = tk.Scale(self.frame, from_=-MAX_A, to=MAX_A, 
                           orient=tk.HORIZONTAL, **kwargs)
        self.ay = tk.Scale(self.frame, from_=MAX_A, to=-MAX_A,
                           orient=tk.VERTICAL, **kwargs)

        #Place scales in lower left corner of canvas.
        self.ax.place(x=l/2+w, y=self.screen[1]-l/2+ZERO)
        self.ay.place(x=ZERO, y=self.screen[1]-l)
    
    def start(self):
        """ Start timer, begin game """
        self.t0 = time.clock()
        self.update()
        
    def update(self):
        #If player is using arrow keys, scales need to be updated.
        self.update_acceleration_scales()
        
        #Scale accelerations with SCALE_A to give meaningful values.
        ax, ay = self.ax.get()/SCALE_A, - self.ay.get()/SCALE_A
        self.user.update(ax, ay) #update players location with accelerations.
        
        t = time.clock() - self.t0
        
        v = self.user.is_position_valid()
        if not v:
            self.label.config(text=TEXT % (self.level, FAIL, t))
            self.frame.bell()
        elif v == END:
            self.label.config(text=TEXT % (self.level, COMPLETE, t))
            self.frame.bell()
        else:
            self.label.config(text=TEXT % (self.level, ELAPSED, t))
            self.frame.after(SPEED, self.update)
            
    def change_level(self, new_level):
        """ 
        Play new level
        new_level: int, level to play.
        """
        self.level = new_level
        self.reset()
        
    def update_acceleration_scales(self):
        """
        Updates accelerations values everytime self.update
        is called based on user changes from arrow keys.
        """
        ay = self.ay.get()
        if self.up:
            if ay + Level.STEP < MAX_A: ay += Level.STEP
            else: ay = MAX_A  
        if self.down:
            if ay - Level.STEP > - MAX_A: ay -= Level.STEP
            else: ay = - MAX_A
        self.ay.set(ay)
        
        ax = self.ax.get()
        if self.left:
            if ax - Level.STEP > - MAX_A: ax -= Level.STEP
            else: ax = - MAX_A
        if self.right:
            if ax + Level.STEP < MAX_A: ax += Level.STEP
            else: ax = MAX_A
        self.ax.set(ax)
        
    def reset(self):
        """ Destroy frame. Reinitialized level. """
        self.frame.destroy()
        try:
            self.__init__(self.master, self.screen, self.level)
            self.start()
        except Exception as e:
            display_error(e.__class__.__name__, str(e))
        
    ### Arrowkey Presses and Releases ###
    def PressKey(self, event):
        """ event binding for pressing game control keys """
        self.Key(event.keysym, True)
    def ReleaseKey(self, event):
        """ event binding for releasing game control keys """
        self.Key(event.keysym, False)            
    def Key(self, key, pressed):
        """
        key: str, keysyms defined globally.
        pressed: bool.
        """
        if key == LEFT: self.left = pressed
        elif key == UP: self.up = pressed
        elif key == RIGHT: self.right = pressed
        elif key == DOWN: self.down = pressed

        
#### METHODS FOR FILEMENU BAR ####
    
def increase_sensitivity():
    """ increase Level.STEP value. """
    if Level.STEP <= 5.0:
        Level.STEP += 0.1
            
def decrease_sensitivity():
    """ increase Level.STEP value. """
    if Level.STEP >= 0.2:
        Level.STEP -= 0.1
        
def toggle_smoke():
    """ Turn on/off the 'smoke' trailing the rocket """
    OnScreenPlayer.SMOKE = False if OnScreenPlayer.SMOKE else True
    
def make_filemenu(master, level):
    """
    Levels - Settings - Help - Exit
    Level bar can change screen to different levels.
    Settings bar can inc/dec sensitivity.
    Help bar can display HELPFILE.
    Exit bar destroys master.
    
    master: tk.Tk object. Main window.
    level: Level object.
    """   
    menubar = tk.Menu(master)
    
    #Display Levels
    filemenu0 = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Levels", menu=filemenu0)
    for l in get_levels():
        #When I tried this without assigning i to l and instead passing l as
        #the argument in level.change_level, it didn't work as intended.
        #I'm not sure why using the i is necessary, but it works.
        filemenu0.add_command(label=str(l), 
                              command=lambda i=l: level.change_level(i))
    
    #Display Settings
    filemenu1 = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Settings", menu=filemenu1)
    filemenu1.add_command(label="Increase Sensitivity", 
                          command=increase_sensitivity)
    filemenu1.add_command(label="Decrease Sensitivity", 
                          command=decrease_sensitivity)  
    filemenu1.add_separator()
    filemenu1.add_command(label="Toggle Smoke", command=toggle_smoke)
    
    #Display Help
    filemenu2 = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=filemenu2)
    filemenu2.add_command(label="How To Play", 
                          command=lambda:os.startfile(HELPFILE))
    #Refresh Button
    menubar.add_command(label="Refresh", command=lambda:play_fullscreen(master))
    #Exit Button
    menubar.add_command(label="Exit", command=master.destroy)

    master.config(menu=menubar)

 
#### PLAY GAME ####
     
def play(screen):
    """
    Begin game at level 0 with a given screen size.
    screen: tuple, (w, h).
    """
    assert screen[0] >= 400, "Screen width minimum is 400."
    assert screen[1] >= 100, "Screen height minimum is 100."
    root = tk.Tk()
    root.resizable(0, 0)
    l = Level(root, screen)
    make_filemenu(root, l)   
    #center window on screen.
    #root.eval('tk::PlaceWindow %s center'%root.winfo_pathname(root.winfo_id())) 

    #Bind keys.
    for key in GAME_CONTROLS:
        root.bind("<%s>" % key, l.PressKey)
        root.bind("<KeyRelease-%s>" % key, l.ReleaseKey)
    root.bind("<%s>" % RESTART, lambda e: l.reset())  
    root.bind("<%s>" % EXIT, lambda event: root.destroy())
                          
    l.start()
    root.mainloop()

def play_fullscreen(root=False):
    """
    Begin game at level 0 in fullscreen.
    root: tk.Tk object. Included so that to restart,
    just have to invoke play_fullscreen with
    whatever the current window was.
    """
    if root: root.destroy()
    root = tk.Tk()
    #find desired screen size.
    root.state("zoomed")
    root.update()
    screen = root.winfo_width(), root.winfo_height()
    l = Level(root, screen)
    make_filemenu(root, l)
    #make full screen.
    root.overrideredirect(True)
    
    #Bind keys.
    for key in GAME_CONTROLS:
        root.bind("<%s>" % key, l.PressKey)
        root.bind("<KeyRelease-%s>" % key, l.ReleaseKey)
    root.bind("<%s>" % RESTART, lambda e: l.reset())  
    root.bind("<%s>" % EXIT, lambda event: root.destroy())
                         
    l.start()
    root.mainloop()


if __name__ == "__main__":
#    #screen: tuple, screen size (w, h).
#    screen = 400, 100
#    play(screen)
    
    play_fullscreen()