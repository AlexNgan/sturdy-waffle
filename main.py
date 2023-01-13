#!/usr/bin/env python3

# Author: Alex.Ngan

import subprocess
import sys
import tkinter as tk
import tkinter.simpledialog as dialog
from tkinter import ttk

import numpy as np
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

#Get location of tkinter widget speficied
def echoLocate(widget):
    x = str(widget.grid_info()["column"])
    y = str(widget.grid_info()["row"])
    print(widget, "at: (" + x + "," + y + ")\n")

#NO WORKY
def who_r_u(widget):
    print("widget name:", str(widget.cget("name")))
    #print("widget name:", widget["name"])

'''
######################################### Code for Sim #########################################
-----------------------------------------------------------------------------------------------
'''
com_ports = [i.device for i in ports.comports()]
PIDs = [i.pid for i in ports.comports()] #List of product IDs (integers unless 'None')
VIDs = [i.vid for i in ports.comports()] #List of vendor IDs (integers unless 'None')

#Array of parameter names and associated values.
params = np.array([
    ["HR:", 72],
    ["SpO2:", 94],
    ["RR:", 15]
])   

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
    hr_value = 72
    spo2_value = 94
    ProSim.ecg.set_ecg_nsra(hr_value) # sets NRS to 72 bpm 
    ProSim.ecg.nsra()           # sends command
    ProSim.spo2.set_spo2_spo2type("MASIM")      #Masimo finger sensor
    ProSim.spo2.set_spo2_sat(spo2_value)
    ProSim.spo2.sat()
    
def desat():
    spo2_value = 85
    ProSim.spo2.set_spo2_sat(spo2_value)
    ProSim.spo2.sat()

    updateVitals(sp=spo2_value)

def changeFiO2():
    fio2 = int(getUserInput("Enter FiO2 value", "FiO2 value needs to be between 21% to 100%"))
    spo2_value = ProSim.spo2.FiO2_adjust(fio2)
    ProSim.spo2.set_spo2_sat(spo2_value)
    ProSim.spo2.sat()

    updateVitals(sp=spo2_value)

def stabilization():
    spo2_value = 91
    ProSim.spo2.set_spo2_sat(spo2_value)
    ProSim.spo2.sat()

    updateVitals(sp=spo2_value)

'''
######################################### Code for GUI #########################################
-----------------------------------------------------------------------------------------------
'''  
window = tk.Tk()
window.option_add("*tearOff", False) # This is always a good idea

# Make the app responsive
window.columnconfigure(index=0, weight=1)
window.columnconfigure(index=1, weight=1)
window.columnconfigure(index=2, weight=1)
window.rowconfigure(index=0, weight=1)
window.rowconfigure(index=1, weight=1)
window.rowconfigure(index=2, weight=1)

# Import the theme tcl file
window.tk.call('source', 'forest-light.tcl')
window.geometry("500x300")
window.title("Fluke ProSim 8 Control Interface")

style = ttk.Style()
ttk.Style(window).theme_use('forest-light')

style.configure("TLabel", font=[('comic sans', 25)])

label1 = ttk.Label(window, name="heading", text="This will control stuff. Current simulated values:")

#Iterates through rows so that automatic element placement doesn't overlap anything.
openRow = 0
openColumn = 0  

def getUserInput(title="Enter value",prompt="Your answer:"):
    input = dialog.askstring(title,prompt)
    return input

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

#Makes the parameters and their values line up.
def initiateVitals():
    global params
    for row in range(params.shape[0]):
        for col in range(params.shape[1]):
            label = ttk.Label(name=params[row,0].shape,text=params[row,col], justify="left")
            label.grid(row=openRow+1,column=0,ipadx=5,ipady=50) #THIS GETS ME THE ALIGNMENT I WANT, BUILD THIS INTO PLACE FUNCTION
            #place(label, openRow+1, 0)
        place(label, getRow(), col)


#NEED TO WRITE A NEW INITITE VITALS THAT ACTUALLY ASSIGNS VALUES TO PRESET LABELS. Can use that old function to assign grid tho?
def updateVitals(hr="72",sp="94",rr="15"):
    global params
    params[0,1] = hr
    params[1,1] = sp
    params[2,1] = rr 
    print(params)
    return params

NewCase()
ProSim = PROSIM(AutoFind(), debug=True)

initiateVitals()

label1.grid(row=0,column=0,columnspan=3)

btn0 = ttk.Button(window, name="start button", text="START", style='Accent.TButton', command=lambda:initial())
btn1 = ttk.Button(window, name="desat button", text="Desat event", command=lambda:desat())
btn2 = ttk.Button(window, name="adjust FiO2 button",text="Change FiO2", command=lambda:changeFiO2())
btn3 = ttk.Button(window, name="stabilize button",text="Patient stable", command=lambda:stabilization())

btn0.grid(row=getRow(), column=0)
btn_row = (btn0.grid_info())["row"]        #Allows placement of other buttons on the same row

btn1.grid(row=btn_row, column=1)
btn2.grid(row=btn_row, column=2)
btn3.grid(row=btn_row, column=3, in_=window)

one = ttk.Label(name="tester1",text="test1")
one.grid(row=0, column=0)
two = ttk.Label(name="tester2",text="test2")
two.grid(row=6, column=6)

window.mainloop()