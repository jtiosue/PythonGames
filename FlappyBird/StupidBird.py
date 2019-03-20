# -*- coding: utf-8 -*-
""" Flappy Bird """

import tkinter as tk
import random

PLAYER_POS_0, PLAYER_WIDTH = (10, 50), 2 #BEFORE SCALING.

INITIAL_V = -3 #Upwards speed when player clicks BEFORE SCALING.
G = 0.2 #acceleration due to gravity BEFORE SCALING.

OBSTACLE_SPEED = -1 #BEFORE SCALING.
WIDTH = 30 #width of openings BEFORE SCALING.
SPEED = 20 #milliseconds between frame updates.
FREQ = 40 #frame updates between obstacles.
CUSHION = 0.2 #adjust for rectangular approximation of oval BEFORE SCALING.


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

        
class Player(object):
    def __init__(self, canvas, screen):
        xscale, yscale = scaling_factor(screen)
        
        self.xcushion, self.ycushion = CUSHION*xscale, CUSHION*yscale
        
        self.x, self.y = PLAYER_POS_0
        self.x *= xscale
        self.y *= yscale
        
        self.w = PLAYER_WIDTH * yscale
        self.player = canvas.create_oval(self.x-self.w, self.y-self.w, 
                                         self.x+self.w, self.y+self.w)
        
        self.vy, self.v0, self.g = 0, INITIAL_V*yscale, G*yscale
        
        self.can, self.screen = canvas, screen
        
    def update(self):
        self.vy += self.g
        self.y += self.vy
        self.can.coords(self.player, self.x-self.w, self.y-self.w, 
                                     self.x+self.w, self.y+self.w) 
    def click(self, event=False):
        self.vy = self.v0
        
    def off_screen(self):
        return self.y - self.w > self.screen[1] or self.y + self.w < 0
        
    def get_rectangle_definition(self):
        x0, y0, x1, y1 = (
                self.x-self.w, self.y-self.w, self.x+self.w, self.y+self.w
        )
        x0, x1 = apply_cushion(x0, x1, self.xcushion)
        y0, y1 = apply_cushion(y0, y1, self.ycushion)
        return x0, y0, x1, y1
    

class Obstacle(object):
    LINE_WIDTH = 2.5
    def __init__(self, canvas, screen):
        xscale, yscale = scaling_factor(screen)
        
        self.x = screen[0]
        self.w = WIDTH * yscale
        
        self.vx = OBSTACLE_SPEED * xscale
        
        opening = random.randint(0, screen[1]-self.w)
        self.top = canvas.create_line(self.x, 0, self.x, opening,
                                      width=Obstacle.LINE_WIDTH*xscale)
        self.bot = canvas.create_line(self.x, opening+self.w, self.x, screen[1],
                                      width=Obstacle.LINE_WIDTH*xscale)
                                      
        self.can, self.screen, self.opening = canvas, screen, opening
                                      
    def update(self):
        self.x += self.vx
        self.can.coords(self.top, self.x, 0, self.x, self.opening)
        self.can.coords(self.bot, self.x, self.opening+self.w, self.x, 
                        self.screen[1])
        
    def off_screen(self):
        return self.x < 0
        
    def destroy(self):
        self.can.delete(self.top)
        self.can.delete(self.bot)


class Home(object):
    def __init__(self, master, screen):
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.can = tk.Canvas(self.frame, width=screen[0], height=screen[1])
        self.can.pack()
        
        self.player = Player(self.can, screen)
        self.obstacles = []
        
        master.bind("<Button-1>", self.player.click)
        master.bind("<space>", self.player.click)
        master.bind("<Return>", self.restart)
        
        self.count, self.score = FREQ, 0
        master.title("Stupid Bird - %d" % self.score)
        
        self.master, self.screen = master, screen
        
        self.update()
    
    def restart(self, event=False):
        self.frame.destroy()
        self.__init__(self.master, self.screen)
        
    def update(self):
        self.player.update()
        #update obstacles and delete them if off screen.
        i = 0
        while i < len(self.obstacles):
            self.obstacles[i].update()
            if self.obstacles[i].off_screen():
                self.obstacles[i].destroy()
                del self.obstacles[i]
                self.score += 1
                self.master.title("Stupid Bird - %d" % self.score)
                i -= 1
            i += 1
        
        #add obstacle if it's time.
        self.count += 1
        if self.count >= FREQ:
            self.obstacles.append(Obstacle(self.can, self.screen))
            self.count = 0
        
        #check to see if the player hit an obstacle or the two hidden borders.
        x0, y0, x1, y1 = self.player.get_rectangle_definition()
        if (len(self.can.find_overlapping(x0, y0, x1, y1)) <= 1 and 
            not self.player.off_screen()):
            self.frame.after(SPEED, self.update)


#### Get rid of Tk icon on window. ####
def make_blank_icon(root):
    """
    root: tk.Tk object.
    give root a blank icon.
    """
    import base64, os
    icondata = base64.b64decode("")
    name = "lskj34.ico"
    with open(name, "wb") as f:
        f.write(icondata)
    try:
        root.wm_iconbitmap(name)
    except: 
        pass
    os.remove(name)
       
def play(screen):
    root = tk.Tk()
    root.title("Stupid Bird")
    root.resizable(0, 0)
    make_blank_icon(root)
    Home(root, screen)
    # root.eval('tk::PlaceWindow %s center'%root.winfo_pathname(root.winfo_id()))
    root.mainloop()
     
if __name__ == "__main__":
    screen = 568, 320
    play(screen)