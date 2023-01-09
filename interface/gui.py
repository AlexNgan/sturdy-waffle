""" 
I'm aware this is jank, that I have to write all the gui code here instead of calling it in the main script but??? 
"""

import tkinter as tk
from tkinter.ttk import *
from tkinter import *

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        #self.pack()
        
    #Application.manual_entry("SpO2")

#call this in main for every parameter, cmd should call specific serial functions?
def button(self,buttontext, color, cmd):
    self.b = tk.Button(self)
    self.b["text"] = buttontext
    self.b["fg"] = color
    self.b["command"] = cmd
    self.b.pack()
    """ b = app.Button(
            text=buttontext,
            command=cmd,
            width=5,
            height=1,
            fg=color, #get hex values for colors
    )
    b.pack() """
    
def manual_entry(parameter):
    value = tk.Entry(text="Enter " + parameter + " value:\n")
    value.pack()
    return value

def label(self, txt):
    heading = Label(
        self, 
        text=txt, 
        height=5,
        width=100
    )
    heading.pack()

def listen(self):
    self.get()

#grab this and slap into main when done?
root = tk.Tk()
root.title("ProSim 8 Vitals Sign Simulator")
heading = label(root,"test")
app = Application(master=root)
ox = manual_entry("SpO2")
spo2 = button(root,"SpO2", "green", NONE)
quit = button(root, "QUIT", "red",root.destroy)

app.mainloop()

