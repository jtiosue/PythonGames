import tkinter as tk
import tkinter.font
import tkinter.messagebox


def _help(cluehistory=False):
    with open("ui/help.txt") as f:
        text = f.read()

    if cluehistory:
        text = "CLUE HISTORY:\n\n" + "\n".join(cluehistory) + "\n\nINSTRUCTIONS:\n\n" + text

    tk.messagebox.showinfo(title="Help", message=text)


class Display(tk.Frame):
    
    def __init__(self, clientsocket, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._game = {}
        self._clientsocket = clientsocket
        
        self._sent_clue, self._recieved_clue = False, False
        self._clue_history = []
        
        options = dict(width=12, height=3)
        
        self._pass_button = tk.Button(
            self, text="Finish turn", command=self._pass_turn, **options
        )
        self._word_entry = tk.Entry(self, justify=tk.CENTER, width=12)
        self._submit_button = tk.Button(
                self, text="Submit", command=self._send_clue, **options
        )
        
        master.bind("<Return>", lambda e: self._submit_button.invoke())            
            
        self._word_buttons = [
            tk.Button(self, **options,
                      command=lambda x=i: self._choose_word(x))
            for i in range(25)
        ]
        
        self._turns_remaining_button = tk.Label(
            self, text="TURNS", **options,
            font=tk.font.Font(size=16, weight="bold")
        )

        tk.Button(
            self, text="Help", **options, 
            command=lambda: _help(self._clue_history)
        ).grid(row=4, column=5)

        options["width"] = 3
        
        self._grid_buttons = [tk.Button(self, **options, 
                                        state=tk.DISABLED) for _ in range(25)]
        
        # grid the buttons
        for r in range(5):
            for c in range(5):
                i = 5*r + c
                self._word_buttons[i].grid(row=r, column=c)
                self._grid_buttons[i].grid(row=r, column=c+6)
            # #space
            # tk.Button(self, **options, highlightbackground="white", highlightthickness=5,
            #           state=tk.DISABLED).grid(row=r, column=5)
            # tk.Button(self, **options, highlightbackground="white", highlightthickness=5,
            #           state=tk.DISABLED).grid(row=r, column=11)
        
        self._turns_remaining_button.grid(row=0, column=5)
        self._pass_button.grid(row=1, column=5)
        self._word_entry.grid(row=2, column=5)
        self._submit_button.grid(row=3, column=5)
        
        self._master = master
        master.title("Awaiting clue from other player")
        
    def _choose_word(self, i):
        if self._recieved_clue and self._game["game_state"] == "ongoing":
            self._send("4" + self._game["words"][i])
        
    def _send_clue(self):
        if (not self._sent_clue and 
            self._game["player"] != self._game["turn"] and
            self._game["game_state"] == "ongoing"):

            clue = self._word_entry.get()
            
            self._send("2" + clue)
            self._clue_history.append("SENT: " + clue)
            
            self._master.title("Awaiting selections from other player")
            self._sent_clue = True
            
    def _new_clue(self, clue):
        if not self._recieved_clue:
            self._recieved_clue = True
#            self._entry(clue)
            self._master.title(
                "Recieved clue '%s', your turn to make selections" % clue
            )
            self._clue_history.append("RECIEVED: " + clue)
    
    def _entry(self, clue):
        self._word_entry.delete(0, tk.END)
        self._word_entry.insert(0, clue)
        
    def _pass_turn(self):
        if (self._game["player"] == self._game["turn"] and 
            self._recieved_clue and
            self._game["game_state"] == "ongoing"):
            
            self._send("3")
            
#            self._master.title("Your turn to send clue")
        
    def _send(self, msg):
        self._clientsocket.send(msg.encode())
        
    def _update_game(self, d):
        self._game.update(d)
        
        if self._game["game_state"] != "ongoing":
            self._entry(self._game["game_state"].upper())
            self._master.title(self._game["game_state"].upper())
            self._submit_button.configure(
                text="Send new game req", command=lambda: self._send("5")
            )
        elif self._game["turn"] !=self._game["player"] and not self._sent_clue:
            self._entry("ENTER CLUE")
            self._master.title("Your turn to send clue")
            self._recieved_clue = False
        elif self._game["turn"] != self._game["player"]:
            self._recieved_clue = False
            self._master.title("Awaiting selections from other player")
        else:
            self._sent_clue = False
            if not self._recieved_clue: 
                self._master.title("Awaiting clue from other player")
            else:
                # Should've already updated the title to contain the clue
                pass
        
            
        self._turns_remaining_button.configure(
                text="TURNS: %d" % self._game["turns_remaining"]
        )
        
        for i in range(25):
            cover = self._game["covers"][i]
            if cover == "b": color = "black"
            elif cover == "g": color = "green"
            elif cover == str(self._game["player"]): color = "red"
            elif cover == "3": color = "blue" # cover = both players
            elif cover != "": color = "yellow" # cover = opposite player
            else: color = "tan"
            self._word_buttons[i].configure(highlightbackground=color, highlightthickness=5)
        
    def _create_game(self, d):
        self._submit_button.configure(text="Submit", command=self._send_clue)
        self._sent_clue, self._recieved_clue = False, False
        self._clue_history = []
        
        self._update_game(d)
        
        
        for i in range(25):
            m = self._game["grid"][i]
            if m == "g": color = "green"
            elif m == "t": color = "tan"
            elif m == "b": color = "black"
            else: color = "red"
            self._grid_buttons[i].configure(highlightbackground=color, highlightthickness=5)
            
            self._word_buttons[i].configure(text=self._game["words"][i])
    
    def recv(self, msg):
        # update visuals based on msg
        m, d = msg[0], msg[1:]
        if m == "0": # game start
            self._create_game(eval(d))
        elif m == "1": # game update
            self._update_game(eval(d))
        elif m == "2": # clue
            if self._game["player"] == self._game["turn"]: self._new_clue(d)
        elif m == "3": # pass turn
            # shouldn't ever recieve this, handled by server.
            pass
        elif m == "4": # word guess
            # shouldn't ever recieve this, handled by server.
            pass
        elif m == "5":
            self._master.title("Player has requested new game")
            self._submit_button.configure(text="New game")
        elif m == "9": # says previous message was invaid
#            self._show_message("invalid previous message: " + d)
            pass
        else: # invalid message
            self._clientsocket.send(("9"+d).encode())
