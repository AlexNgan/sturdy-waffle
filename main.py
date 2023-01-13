#!/usr/bin/env python3

# Author: Alex.Ngan

import subprocess
import sys
import tkinter as tk
import tkinter.simpledialog as dialog
from datetime import datetime
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
    print(widget, "at: (" + x + "," + y + ")/n")

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
                print("Fluke Pro Sim 8 found at:", com_ports[i], "/n")
                return com_ports[i]
        else:
            print("No Device Found. Please confirm that the simulator is plugged into this computer./n")
            continue 

def UpdateVitals():
    global params
    hr_label = ttk.Label(window, name="hr",text=("HR:",params[0,1]))
    sp_label = ttk.Label(window, name="spo2",text=("SpO2:",params[1,1]))
    rr_label = ttk.Label(window, name="rr",text=("RR:",params[2,1]))

    hr_label.grid(row=3,column=3)
    sp_label.grid(row=4,column=3)
    rr_label.grid(row=5,column=3)

def ChangeVitals(hr=72,sp=94,rr=15):
    global params
    params[0,1] = hr
    params[1,1] = sp
    params[2,1] = rr
    UpdateVitals()
    print(params)
    return params

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
    ChangeVitals(sp=spo2_value)

def changeFiO2():
    fio2 = int(getUserInput("Enter FiO2 value", "FiO2 value needs to be between 21% to 100%"))
    spo2_value = ProSim.spo2.FiO2_adjust(fio2)
    ProSim.spo2.set_spo2_sat(spo2_value)
    ProSim.spo2.sat()
    ChangeVitals(sp=spo2_value)

def stabilization():
    spo2_value = 91
    ProSim.spo2.set_spo2_sat(spo2_value)
    ProSim.spo2.sat()
    ChangeVitals(sp=spo2_value)

'''
######################################### Code for GUI #########################################
-----------------------------------------------------------------------------------------------
'''  
window = tk.Tk()
#window.option_add("*tearOff", False) # This is always a good idea

# Make the app responsive
window.columnconfigure(index=0, weight=1, minsize=10)
window.columnconfigure(index=1, weight=1)
window.columnconfigure(index=2, weight=1)
window.columnconfigure(index=3, weight=1)
window.columnconfigure(index=4, weight=1)
window.columnconfigure(index=5, weight=1)
window.columnconfigure(index=7, weight=1, minsize=10)
window.rowconfigure(index=0, weight=0, minsize=30)
window.rowconfigure(index=1, weight=0)
window.rowconfigure(index=2, weight=0, minsize=30)
window.rowconfigure(index=3, weight=0)
window.rowconfigure(index=4, weight=0)
window.rowconfigure(index=6, weight=0, minsize=30)
window.rowconfigure(index=7, weight=0)


#Import the theme tcl file
window.tk.call('source', 'C:/Users/Alex.Ngan/OneDrive - Zoll Medical Corporation (1)/Documents/sturdy-waffle/forest-light.tcl')
window.geometry("500x500")
window.title("Fluke ProSim 8 Control Interface")

style = ttk.Style()
ttk.Style(window).theme_use('forest-light')
style.configure("TLabel", justify="center")

def getUserInput(title="Enter value",prompt="Your answer:"):
    input = dialog.askstring(title,prompt)
    return input

NewCase()
UpdateVitals()
ProSim = PROSIM(AutoFind(), debug=True)

heading = ttk.Label(window, name="heading", text="This program controls a Fluke ProSim8 Vitals Simulator. \nCurrent simulated values:")
heading.grid(row=1,column=0,columnspan=6)

btn0 = ttk.Button(window, name="start button", text="START", style='Accent.TButton', command=lambda:initial())
btn1 = ttk.Button(window, name="desat button", text="Desat event", command=lambda:desat())
btn2 = ttk.Button(window, name="adjust FiO2 button",text="Change FiO2", command=lambda:changeFiO2())
btn3 = ttk.Button(window, name="stabilize button",text="Patient stable", command=lambda:stabilization())

btn0.grid(row=7, column=1)
btn1.grid(row=7, column=2)
btn2.grid(row=7, column=4)
btn3.grid(row=7, column=5)

window.mainloop()