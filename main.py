#!/usr/bin/env python3

#The main code will live here, functions will be mapped to keys
import subprocess
import sys
import tkinter as tk
from tkinter import ttk

import numpy as np
import serial
import serial.tools.list_ports as ports
from serial.tools.list_ports import comports

from prosim8.prosim import PROSIM

'''
**********  These are tools/functions to debug, if necessary.  **********
'''
#Tool to check if this directory is on path and append if needed
def PATHcheck(directory):
    sys.path.append(directory)

    for line in sys.path:
        print(line)

#Clears the shell.
def NewCase():
    subprocess.run("cls", shell=True, check=True) 


'''
######################################### Code for Sim #########################################
-----------------------------------------------------------------------------------------------
'''
com_ports = [i.device for i in ports.comports()]
PIDs = [i.pid for i in ports.comports()] #List of product IDs (integers unless 'None')
VIDs = [i.vid for i in ports.comports()] #List of vendor IDs (integers unless 'None')

global ProSim

#Function to autodetect and connect to first COM port that matches the ProSim 8
def AutoFind():  
    for i in range(len(com_ports)): 
        if VIDs[i] is not None:
            if (VIDs[i] == 1027) & (PIDs[i] == 24577):
                print("Fluke Pro Sim 8 found at:", com_ports[i], "\n")
                return com_ports[i]
        else:
            print("No Device Found. Please confirm that the simulator is plugged into this computer.\n")
            continue

def initial():
    ProSim.spo2.set_spo2_sat(85)

def changeFiO2():
    entry = ttk.Entry(text="New FiO2:")
    entry.place(entry, getRow(), getColumn())
    ProSim.spo2.FiO2_adjust(input)

    #App.manual_entry("SpO2")

'''
######################################### Code for GUI #########################################
-----------------------------------------------------------------------------------------------
'''  
class App(object):
    def __init__(self):
        super().__init__()

        style =ttk.Style(self)

        '''
        Label styling.
        '''
        style.configure("TLabel",
            font="comic sans")

        #Refreshes window with any changes.
        def refresh():
            tk.Tk().update()

        #Function to arrange elements in grid w default values.
        def place(element, row=0, column=0, pad=5):
            element.grid(row=row, column=column, pady=pad)


window = tk.Tk()
window.geometry("500x300")
window.title("Fluke ProSim 8 Control Interface")
style = ttk.Style()

lbl = ttk.Label(text="This will control stuff. Current simulated values:", anchor="w")

#Iterates through rows so that automatic element placement doesn't overlap anything.
openRow = 0
openColumn = 0

#Array of parameter names and associated values.
params = np.array([
    ["HR:", 72],
    ["RR:", 15],
    ["SpO2:", 85]
])     


def updateMsg():
    global sysmsg
    #sysmsg = str(message)
    sysmsg = tk.Message(window, text="Button Pressed.")
    sysmsg.grid(row=getRow(), column=3)

def getRow():
    global openRow
    openRow = openRow+1
    return openRow

def getColumn():
    global openColumn
    openColumn = openColumn+1
    return openColumn

lbl = ttk.Label(text="This will control stuff. Current simulated values:", anchor="w")
btn = ttk.Button(text="SEND", command=updateMsg())
#task = ttk.Checkbutton(text="Task 1")

#Map function for dynamic changes based on state.
style.map("TButton",
    foreground=[('pressed', 'red'), ('active', 'blue')],
    background=[('pressed', '!disabled', 'black'), ('active', 'white')]
    )

#Configure function for basic formatting.    
style.configure("TButton", 
    padding=10, 
    relief="flat",
    background="#ccc",
    font=[("arial", 7,"bold")]
    )

style.configure("TLabel",
    borderwidth=5,
    relief="flat",
    anchor="w" #options are compass based
    )

#Function to arrange elements in grid w default values.
def place(element, row=0, column=0, pad=5):
    element.grid(row=row, column=column, pady=pad)

lbl.grid(
    row=0,
    column=0,
    columnspan=3,
    padx=50,
    pady=10
    )

#Makes the parameters and their values line up.
for row in range(params.shape[0]):
    for col in range(params.shape[1]):
        label = ttk.Label(text=params[row,col], justify="left")
        label.grid(sticky="E", row=openRow+1,column=0) #THIS GETS ME THE ALIGNMENT I WANT, BUILD THIS INTO PLACE FUNCTION
        #place(label, openRow+1, 0)
    place(label, getRow(), col)

NewCase()
ProSim = PROSIM(AutoFind(), debug=True)
#place(btn, getRow())
#task.grid(row=getRow(), column=2)
#window.messagebox.askyesnocancel(title=None, message=None, **options)

lbl = ttk.Label(text="This will control stuff. Current simulated values:", anchor="w")
btn = ttk.Button(text="SEND", command=updateMsg())
#task = ttk.Checkbutton(text="Task 1")
sysmsg = tk.Message(window, text="")

btn.grid(row=getRow(), column=0, columnspan=2)
btn_row = (btn.grid_info())["row"]

sysmsg.grid(row=getRow(), column=3)
window.mainloop()