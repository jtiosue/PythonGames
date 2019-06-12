import tkinter as tk
import time


PROPERTIES = {
    "ice shifts": (0, 1), "end ice shifts": (0, 2),
    "goals": (1, 0), "assists": (1, 1), "plus": (1, 2), "minus": (1, 3), 
    "shots": (2, 0), "blocked shots": (2, 1), "off-target shots": (2, 2),
    "hits": (2, 3)
}

STOP_SHIFT = "plus", "minus", "end ice shifts"
START_SHIFT = "ice shifts",
PLUS = "goals", "assists"


class Note:
    def __init__(self, master):
        self.valid, self.text = False, ""
        self.message = tk.Text(master, width=40, height=10)
        self.message.focus_force()
        self.message.grid()
        
    def complete(self):
        self.valid = True
        self.text = self.message.get("1.0", tk.END)
        self.destroy()
        
    def destroy(self):
        self.message.master.destroy()
        
    def insert(self, contents):
        self.message.insert("1.0", contents)
        self.text = contents

        
def note(contents=None):
    root = tk.Tk()
    root.resizable(False, False)
    root.focus_force()
    root.title("")
    n = Note(root)
    root.bind("<Escape>", lambda e: n.destroy())
    if contents: 
        n.insert(contents)
        n.message.config(height=40, width=70)
        n.valid = True
    else:
        root.bind("<Return>", lambda e: n.complete())
    root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
    root.mainloop()
    if n.valid: return n.text


class Button(tk.Button):
    def __init__(self, master, prop, command):
        super().__init__(
            master, text=prop+"\n0", command=command,
            width=20
        )
        self.val, self.prop = 0, prop
        
    def increment(self):
        self.val += 1
        self.config(text="%s\n%d" % (self.prop, self.val))
        
    def __str__(self):
        return "%s: %d" % (self.prop, self.val)



class Window(tk.Frame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_ice = False
        self.toi_per_shift = 0
        self.master.title("not on ice")
        self.toi, self.t0 = 0, 0
        self.paused = False
        self.toi_per_shift_button = tk.Button(
            self, text="PAUSE\ntoi/shift: %g sec" % 0, width=20,
            command=self.pause
        )
        self.toi_per_shift_button.grid(row=0, column=0)
        self.master.bind("<space>", lambda e: self.pause())
        
        self.properties = {
            x: Button(self, x, command=lambda i=x: self.button_press(i)) 
            for x in PROPERTIES
        }
        for p in PROPERTIES:
            self.master.bind(
                "<%s>" % p[0], lambda e, i=p: self.button_press(i)
            )
            
            row, column = PROPERTIES[p]
            self.properties[p].grid(row=row, column=column)
            
        self.notes = []
        
        tk.Button(
            self, width=20, text="NOTE\n", command=self.new_note
        ).grid(row=0, column=3)
        self.master.bind("<n>", lambda e: self.new_note())
        
        tk.Label(
            self, wraplength=600, justify=tk.LEFT, text=(
                "The spacebar is equivalent to pressing the pause button. "
                "Otherwise, either click each button or press the first letter"
                " of the button command on the keyboard. Pressing 'n' or "
                "clicking the note button opens a new window. After typing the"
                " note, to discard, exit or press 'escape'; to keep the note, "
                " press enter."
            )
        ).grid(row=3, column=0, columnspan=4)
        
    def pause(self):
        if not self.on_ice: return
        if self.paused:
            self.paused = False
            self.t0 = time.time()
            self.master.title("on ice")
        else:
            self.toi += time.time() - self.t0
            self.paused = True
            self.master.title("paused")
        
    def new_note(self):
        n = note()
        if n: self.notes.append(n)
        
    def button_press(self, p):        
        if p not in START_SHIFT and not self.on_ice: return
        elif p in START_SHIFT and self.on_ice: return
        
        if p in STOP_SHIFT:
            if self.paused and p in PLUS + ("plus", "minus"): return
            self.master.title("not on ice")
            if not self.paused: 
                self.toi += time.time() - self.t0
            self.on_ice, self.paused = False, False
            self.toi_per_shift = self.toi / self.properties["ice shifts"].val
            self.toi_per_shift_button.config(
                text="PAUSE\ntoi/shift: %g sec" % round(self.toi_per_shift)
            )
            if p != "end ice shifts": 
                self.properties["end ice shifts"].increment()
            
        elif p in START_SHIFT:
            self.master.title("on ice")
            self.on_ice = True
            self.t0 = time.time()
            
        if p in PLUS and not self.paused:
            self.button_press("plus")
            
        if p in self.properties and not self.paused: 
            self.properties[p].increment()
            
            
    
    def __str__(self):
        self.properties.pop("end ice shifts", 0)
        s = "toi/shift: %g\n" % round(self.toi_per_shift)
        for p in PROPERTIES:
            if p in self.properties: s += str(self.properties[p]) + "\n"
        if not self.notes: return s
        s += "\nNOTES\n"
        for n in reversed(self.notes):
            s += "\n- " + n

        return s
    
        
       
def main():
    root = tk.Tk()
    root.resizable(False, False)
    root.title("")
    root.focus_force()
    root.bind("<Escape>", lambda e: root.destroy())
    frame = Window(root)
    frame.grid()
    frame.focus_force()
    root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
    root.mainloop()
    print(note(str(frame)))
    
    
    
if __name__ == "__main__":
    main()