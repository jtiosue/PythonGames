# -*- coding: utf-8 -*-
"""
Penguin Drop - Don't let the ice break!
Tip: You have to hit the penguins; hitting a parachute will do nothing!
"""

###### SETTINGS ######

### Adjust window ###
SCREEN = 1200, 700  #Canvas size in pixels.

### Adjust difficulty ###
MAX_PENGUINS = 10  #Max number of penguins before ice breaks.

### Adjust controls ###
GAME_CONTROLS = LEFT, RIGHT, SHOOT = "<Left>", "<Right>", "<space>"
RESTART = "<Return>"

### Adjust movement of objects ###
FALLING_SPEED = 1.2  #Speed that penguins fall.
G = 0.1  #Acceleration of cannonball down due to gravity.
START_VELOCITY = 23  #Magnitude of velocity of cannonball when first shot.

### Adjust relative sizes of objects ###
PERCENT_ICE = 0.15  #Ice height in terms of percent of screen.
PERCENT_PENGUIN = 0.05  #Penguin height in terms of percent of screen.
PERCENT_PARACHUTE = 0.07  #Parachute height in terms of percent of screen.
PERCENT_CANNONBALL = 0.007  #Cannonball radius in terms of percent of screen.
PERCENT_CANNON = 0.08  #Cannon height in terms of percent of screen.
## Penguin, parachute, and cannon images are scaled to keep their aspect ratios.
## Ice image is set at size = (SCREEN[0], PERCENT_ICE*SCREEN[1])

### Adjust frame rate ###
SPEED = 20  #Milliseconds between screen redraw.

###############################################################################

import os, math, random
from PIL import Image, ImageTk

if os.sys.version_info.major > 2:
    xrange = range
    import tkinter as tk
else:
    import Tkinter as tk

#### Image filenames ####

FAVICON = "images/favicon.ico"

ICE = "images/ice.png"
PENGUIN = "images/penguin.png"
PARACHUTE = "images/parachute.png"

## There are multiple cannon images, each named with an
## integer that represents the angle that they are offset.
CANNON_DIRECTORY = "images/cannon/"
CANNON = CANNON_DIRECTORY + "%d.png"  #%d is for the angle.
## i.e. a cannon image at 100 degrees has filename = CANNON % 100

#### Colors ####
SKY_COLOR = "#9fd7fb"
CANNONBALL_COLOR = "white"  #Snowball!


#### Method for creating and sizing PIL.Images ####

def create_image(filename, width=0, height=0):
    """
    Returns a PIL.Image object from filename - sized
    according to width and height parameters.

    filename: str.
    width: int, desired image width.
    height: int, desired image height.
    
    1) If neither width nor height is given, image will be returned as is.
    2) If both width and height are given, image will resized accordingly.
    3) If only width or only height is given, image will be scaled so specified
    parameter is satisfied while keeping image's original aspect ratio the same. 
    """
    #Create a PIL image from the file.
    img = Image.open(filename, mode="r")
    
    #Resize if necessary.
    if not width and not height:
        return img
    elif width and height:
        return img.resize((int(width), int(height)), Image.ANTIALIAS)
    else:  #Keep aspect ratio.
        w, h = img.size
        scale = width/float(w) if width else height/float(h)
        return img.resize((int(w*scale), int(h*scale)), Image.ANTIALIAS)
 
#### Create cannon PIL images and sort them based on angle ####
   
def create_cannons():
    """
    returns tuple of length 2:
        first argument: list of sorted angles (in radians).
        second argument: list of PIL images that map to their list of angles.
        
    Each cannon image has an integer name that represents
    the angle (in degrees) that it is offset.
    """
    angles = []
    for filename in os.listdir(CANNON_DIRECTORY):
        try: 
            if os.path.isfile(CANNON_DIRECTORY+filename):
                angles.append(int(filename.split(".")[0]))

        except ValueError: pass
    angles.sort()
    
    images = []
    for a in angles:
        images.append(create_image(CANNON % a, height=PERCENT_CANNON*SCREEN[1]))
        
    return [math.radians(a) for a in angles], images


#### On screen objects ####

class Parachute(object):
    """
    Deals with the animation of a parachute on canvas.
    canvas: tk.Canvas object to draw on.
    initial_position: tuple, initial position of center of image (x, y).
    """
    #Create image just once upon class creation. Use same image throughout.
    image = create_image(PARACHUTE, height=PERCENT_PARACHUTE*SCREEN[1])
    def __init__(self, canvas, initial_position):
        self.x, self.y = initial_position
        self.can = canvas
        
        #Must be created AFTER main window has been opened.
        photo = ImageTk.PhotoImage(image=Parachute.image)
        
        #So the photo doesn't disappear!!
        self.label = tk.Label(image=photo)
        self.label.image = photo
        
        #Draw parachute on canvas.
        self.parachute = self.can.create_image((self.x, self.y), image=photo)
        
    def destroy(self):
        """ Destroy the parachute on canvas and the label remembering it. """
        if self.parachute:
            self.can.delete(self.parachute)
            self.label.destroy()
            self.parachute, self.label = False, False
        
    def update(self):
        """ Update the parachutes position and redraw it. """
        self.y += FALLING_SPEED
        self.can.coords(self.parachute, self.x, self.y)


class Penguin(object):
    """ 
    Deals with the animation of the penguin on canvas.
    canvas: tk.Canvas object to draw on.
    """
    #Create image just once upon class creation. Use same image throughout.
    image = create_image(PENGUIN, height=PERCENT_PENGUIN*SCREEN[1])
    def __init__(self, canvas):
        self.can = canvas
        
        self.w, self.h = Penguin.image.size
        
        #Must be created AFTER main window has been opened.
        photo = ImageTk.PhotoImage(image=Penguin.image)
        
        #So the photo doesn't disappear!!
        self.label = tk.Label(image=photo)
        self.label.image = photo
        
        #Initial position: above screen at random x value.
        self.x, self.y = random.randint(0, SCREEN[0]), -self.h
        
        #Draw on canvas.
        self.penguin = self.can.create_image((self.x, self.y), image=photo)
        #Create the parachute animation that goes with the penguin.
        self.parachute = Parachute(self.can, (self.x, self.y-self.h))
        
    def destroy_parachute(self):
        """ Destroy the parachute """
        self.parachute.destroy()
        self.parachute = False
        
    def update(self):
        """ Update the penguins position, redraw penguin and parachute. """
        self.y += FALLING_SPEED
        self.can.coords(self.penguin, self.x, self.y)
        if self.parachute: self.parachute.update()
        
    def destroy(self):
        """ Destroy both the parachute and the penguin. """
        self.can.delete(self.penguin)
        self.label.destroy()
        self.destroy_parachute()
        
    def get_overlapping(self):
        """ Return list of canvas objects that are overlapping the penguin. """
        x0, y0 = self.x - self.w/2, self.y - self.h/2
        x1, y1 = self.x + self.w/2, self.y + self.h/2
        return self.can.find_overlapping(x0, y0, x1, y1)
        
    def off_screen(self):
        """ Returns True if penguin has fallen below the screen, else False. """
        #Add a little cushion; make sure it's completely off screen.
        return self.y - self.h - PERCENT_PARACHUTE*SCREEN[1] > SCREEN[1]
        
        
class Ice(object):
    """
    Deals with the ice.
    canvas: tk.Canvas object to draw on.
    """
    #Create image just once upon class creation. Use same image throughout.
    image = create_image(ICE, width=SCREEN[0], height=PERCENT_ICE*SCREEN[1])
    def __init__(self, canvas):
        self.can = canvas
        
        #Must be created AFTER main window has been opened.
        photo = ImageTk.PhotoImage(image=Ice.image)
        
        #So the photo doesn't disappear!!
        label = tk.Label(image=photo)
        label.image = photo
        
        height = Ice.image.size[1]
        self.x, self.y = SCREEN[0]/2, SCREEN[1]-height/2
        self.ice = self.can.create_image((self.x, self.y), image=photo)
        
        #Keeps track of penguins standing on the ice.
        self.penguins = []
        
    def fall(self):
        """
        When too many penguins are on the ice, the ice breaks
        and all the penguins fall. If the ice and penguins have
        fallen below screen already, do nothing.
        """
        ## Should be faster than
        ## if not all(p.off_screen() for p in self.penguins):
        if any(not p.off_screen() for p in self.penguins):
            self.y += FALLING_SPEED
            self.can.coords(self.ice, self.x, self.y)
            
            for p in self.penguins:
                p.update()
        
    def get_ice(self):
        """ Returns tk.Canvas.create_image object. """
        return self.ice
    
    def add_penguin(self, penguin):
        """ Add another penguin standing on the ice. """
        self.penguins.append(penguin)
        
    def get_num_penguins(self):
        """ Returns number of penguins standing on the ice. """
        return len(self.penguins)


class Cannonball(object):
    """
    Deals with the animation of the cannonballs.
    canvas: tk.Canvas object to draw on.
    initial_position: tuple, (x, y).
    initial_velocity: tuple, (vx, vy).
    """
    def __init__(self, canvas, initial_position, initial_velocity):
        self.can = canvas
        self.x, self.y = initial_position
        self.vx, self.vy = initial_velocity
        
        self.w = PERCENT_CANNONBALL*min(SCREEN)
        
        self.cannonball = self.can.create_oval(self.x-self.w, self.y-self.w,
                                               self.x+self.w, self.y+self.w,
                                               fill=CANNONBALL_COLOR)                                       
    def destroy(self):
        """ Destroys the cannonball from the canvas. """
        self.can.delete(self.cannonball)
    
    def update(self):
        """ Updates position on screen. """
        self.x += self.vx
        
        self.vy += G
        self.y += self.vy
        
        self.can.coords(self.cannonball, self.x-self.w, self.y-self.w,
                                         self.x+self.w, self.y+self.w)
                                   
    def off_screen(self):
        """ Returns True if the cannonball is off the screen; else False. """
        return (self.x - self.w > SCREEN[0] or self.x + self.w < 0 or
                self.y - self.w > SCREEN[1] or self.y + self.w < 0)
                
    def get_cannonball(self):
        """ Returns a tk.Canvas.create_oval object. """
        return self.cannonball

                
class Home(object):
    """
    Deals with all the penguins and cannonballs. 
    Adds new penguins at increasing frequency.
    canvas: tk.Canvas object to draw on.
    ice: Ice object.
    """
    def __init__(self, canvas, ice):
        self.can, self.ice = canvas, ice
        
        #Starting probability of new penguins and how much to increase it by.
        self.prob, self.increment = 0.02, 0.005
        
        #Starting count and at what count to increment the probability.
        self.count, self.max_count = 0, 10000/SPEED
        
        self.score = 0 #Everytime cannonball hits a penguin, score + 1.
        
        self.penguins = [Penguin(self.can)] #list of Penguin objects.
        self.cannonballs = [] #list of Cannonball objects.
        
    def update_cannonballs(self):
        """ Update cannonball positions, destroy if off screen. """
        i = 0
        while i < len(self.cannonballs):
            b = self.cannonballs[i]
            b.update()
            if b.off_screen(): #if it's off screen, destroy.
                b.destroy()
                self.cannonballs.pop(i)
            else:
                i += 1
                
    def update_penguins(self):
        """
        Update positions of penguins and check if hit by cannonball. 
        Destroys both penguin and cannonball when hit.
        """
        i = 0
        while i < len(self.penguins):
            p = self.penguins[i]
            p.update()
            overlapping = p.get_overlapping()
            #if it's on the ice, add it to self.ice.
            if self.ice.get_ice() in overlapping:
                p.destroy_parachute()
                self.ice.add_penguin(p)
                self.penguins.pop(i)
                i -= 1  
            elif p.off_screen():
                p.destroy()
                self.penguins.pop(i)
                i -= 1
            else: #Check if any cannonballs are hitting the penguin.
                for n in xrange(len(self.cannonballs)):
                    if self.cannonballs[n].get_cannonball() in overlapping:
                        self.score += 1
                        self.cannonballs[n].destroy()
                        self.cannonballs.pop(n)
                        p.destroy()
                        self.penguins.pop(i)
                        i -= 1
                        break #Only one cannonball is destroyed per penguin.
            i += 1
        
    def update(self):
        """ Update cannonballs, penguins, game. """
        self.update_cannonballs()
        self.update_penguins()
        
        ## Update game difficulty and/or add penguins.
        
        self.count += 1
        
        if random.random() <= self.prob:
            self.penguins.append(Penguin(self.can))
            
        if self.count >= self.max_count:
            if self.prob + self.increment < 1:
                self.prob += self.increment
            else:
                self.prob = 1
            self.count = 0
            
    def add_cannonball(self, cannonball):
        """ cannonball: Cannonball object. """
        self.cannonballs.append(cannonball)
        
    def get_score(self):
        """ Score: int, how many penguins have been killed. """
        return self.score
        

class Cannon(object):
    """
    Deals with the cannon animation the screen.
    When fired, adds cannonball to Home class.
    canvas: tk.Canvas object/
    home: Home object.
    """
    #Create images just once upon class creation. Use same images throughout.
    #angles (in radians) is sorted and maps directly to its image in images.
    angles, images = create_cannons()
    def __init__(self, canvas, home):
        self.can, self.home = canvas, home
        self.position = (SCREEN[0]/2, #x = middle of screen.
                         SCREEN[1]-(SCREEN[1]*PERCENT_ICE)) #y = ontop of ice.
        
        #Cannon.angles and self.photos indices map accordingly.
        self.photos = [ImageTk.PhotoImage(image=img) for img in Cannon.images]
        
        ### For example: Cannon.angles[i] == angle of self.photos[i] ###
        
        #self.index follows what photo and angle is current.
        self.index = len(Cannon.angles)//2 #start in the middle.
        self.current_image = False
        
        self.draw()
    
    def destroy(self):
        """ Deletes any cannon image from the canvas. """
        if self.current_image:
            self.can.delete(self.current_image)
            
    def draw(self):
        self.destroy()
        self.current_image = self.can.create_image(
                self.position, image=self.photos[self.index]
        )
    def rotate_ccw(self):
        """ Changes current cannon to next one ccw """
        if self.index + 1 < len(self.angles):
            self.index += 1
            self.draw()
            
    def rotate_cw(self):
        """ Changes current cannon to next one ccw """
        if self.index > 0:
            self.index -= 1
            self.draw()
            
    def shoot_cannonball(self):
        """ 
        Computes the initial position and initial velocity of the cannonball
        based on the current cannon position and angle. With that, creates a 
        Cannonball object and adds it to self.home to be integrated into game.
        """
        angle = Cannon.angles[self.index]
        vx = START_VELOCITY * math.cos(angle)
        vy = -START_VELOCITY * math.sin(angle)
        
        #Get approximate length of barrel.
        l = SCREEN[1]*PERCENT_CANNON/2.0
        x = self.position[0] + (math.cos(angle)*l)
        y = self.position[1] - (math.sin(angle)*l/2.0)

        self.home.add_cannonball(Cannonball(self.can, (x, y), (vx, vy)))
        

class Game(object):
    """ 
    Creates a tk.Frame and a tk.Canvas to draw on.
    Initializes Ice, Home, and Cannon objects.
    Binds game keys.
    Updates the game every SPEED milliseconds.
    
    master: tk.Tk window.
    """
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.can = tk.Canvas(self.frame, width=SCREEN[0], 
                             height=SCREEN[1], bg=SKY_COLOR)
        self.can.pack()
        
        self.ice = Ice(self.can)
        self.home = Home(self.can, self.ice)
        self.cannon = Cannon(self.can, self.home)
        
        #Binding game keys to rotate and fire cannon.
        master.bind(SHOOT, lambda event: self.cannon.shoot_cannonball())
        master.bind(LEFT, lambda event: self.cannon.rotate_ccw())
        master.bind(RIGHT, lambda event: self.cannon.rotate_cw())
        
        self.master, self.playing = master, False
        
    def restart(self):
        """ Destroys the current frame, makes a new one, begins game. """
        self.frame.destroy()
        self.__init__(self.master)
        self.start()
        
    def update(self):
        """
        Update self.home which updates all the penguins and cannonballs.
        Check if game is lost - if so, destroy the cannon image and unbind
        cannon operators (GAME_CONTROLS). Start making the ice fall.
        """
        self.home.update()
        
        self.master.title("Penguin Drop - %d" % self.home.get_score())
        
        if self.ice.get_num_penguins() > MAX_PENGUINS: #If game is lost.
            self.ice.fall()
            
            #If it's just been lost, destroy the cannon and take away controls.
            if self.playing:
                self.playing = False
                self.cannon.destroy()
                for key in GAME_CONTROLS:
                    self.master.unbind(key)
                
        self.frame.after(SPEED, self.update)
        
    def start(self):
        """ Begin Game """
        self.playing = True
        self.update()


def main():
    """ Open a window - Play Game """
    root = tk.Tk()
    root.wm_iconbitmap(FAVICON)
    root.resizable(0, 0)
    game = Game(root)
    
    #Bind RESTART key to restart game at any time.
    root.bind(RESTART, lambda event: game.restart())
    
    #Place window in center of screen.
    #root.eval('tk::PlaceWindow %s center'%root.winfo_pathname(root.winfo_id()))
    
    game.start()
    root.mainloop()
    
    
if __name__ == "__main__":
    main()