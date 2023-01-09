#!/usr/bin/env python3

#The main code will live here, functions will be mapped to keys
import subprocess
import sys
import serial
import serial.tools.list_ports as ports
from serial.tools.list_ports import comports
from prosim8.prosim import PROSIM
import tkinter as tk
from tkinter.ttk import *
from tkinter import *

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
**********  "Actual" code lives below this.  **********
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
                #PROSIM.port = com_ports[i]
                print("Fluke Pro Sim 8 found at:", com_ports[i], "\n")
                # change com port when connected
                return com_ports[i]
        else:
            print("No Device Found. Please confirm that the simulator is plugged into this computer.\n")
            continue

def MakeUI(self):
    window = Application()
    window.label()
    window.quit = tk.Button(
        text="QUIT", fg="red",
        command=self.master.destroy
        )
    gui.button("Task(s) 1-3", "green", )
    #Application.manual_entry("SpO2")

NewCase()
AutoFind()
ProSim = PROSIM(AutoFind(), debug=True)
ProSim.spo2.set_spo2_sat(69) 
ProSim.spo2.sat()
ProSim.ecg.ecgrun() # turn on ECG 