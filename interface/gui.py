""" 
I'm aware this is jank, that I have to write all the gui code here instead of calling it in the main script but??? 
"""

import tkinter as tk
from tkinter import ttk
import numpy as np

class App(object):
    def __init__(self):
        super().__init__()

        self.geometry("200x200")

        style =ttk.Style(self)

        '''
        Place below into class when testing is done. Instantiate App in main.py
        '''
        window = tk.Tk()
        window.geometry("300x300")
        window.title("Fluke ProSim 8 Control Interface")
        style = ttk.Style()

        #Iterates through rows so that automatic element placement doesn't overlap anything.
        openRow = 0
        openColumn = 0

        def getRow():
            global openRow
            openRow = openRow+1
            return openRow

        def getColumn():
            global openColumn
            openColumn = openColumn+1
            return openColumn

        #Function to arrange elements in grid w default values.
        def place(element, row=0, column=0, pad=5):
            element.grid(row=row, column=column, pady=pad)

        def manual_entry(parameter):
            value = tk.Entry(text="Enter " + parameter + " value:\n")
            value.pack()
            return value

        def listen(self):
            self.get()

        '''
        Label styling.
        '''
        style.configure("TLabel",
            font="comic sans")
        
        #Map function for dynamic changes based on state.
        style.map("TButton",
            foreground=[('pressed', 'red'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'black'), ('active', 'white')]
        )

        #Configure function for basic formatting.    
        style.configure("TButton", 
            padding=6, 
            relief="flat",
            background="#ccc",
            font=[("arial", 7,"bold")]
        )

        style.configure("TLabel",
            borderwidth=5,
            relief="flat",
            anchor="w" #options are compass based
        )

        #Refreshes window with any changes.
        def refresh():
            tk.Tk().update()

        #Function to arrange elements in grid w default values.
        def place(element, row=0, column=0, pad=5):
            element.grid(row=row, column=column, pady=pad)
