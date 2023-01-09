#!/usr/bin/env python3

#The main code will live here, functions will be mapped to keys
import subprocess
import sys
import serial
import serial.tools.list_ports as ports
from serial.tools.list_ports import comports

'''
**********  These are tools/functions to debug, if necessary.  **********
'''
#Tool to check if this directory is on path and append if needed
def PATHcheck(directory):
    sys.path.append(directory)

    for line in sys.path:
        print(line)

def NewCase():
    subprocess.run("cls", shell=True, check=True) #Clears the shell.

#See which modules are able to be imported.
def GetModules():
    results = [m.__name__ for m in sys.modules.values() if m]
    results = sorted(results)
    print(results)


'''
**********  "Actual" code lives below this.  **********
'''
com_ports = [i.device for i in ports.comports()]
#com_ports = [str(i) for i in ports.comports()]# create a list of ['COM1','COM2'] as str
PIDs = [i.pid for i in ports.comports()] #List of product IDs (integers unless 'None')
VIDs = [i.vid for i in ports.comports()] #List of vendor IDs (integers unless 'None')

PROSIM = serial.Serial(
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            xonxoff=False,
            rtscts=True, 
            dsrdtr=True,
            timeout=0.5,
            write_timeout=0.5
        )

#Function to autodetect and connect to first COM port that matches the ProSim 8
def AutoFind():  
    for i in range(len(com_ports)): 
        if VIDs[i] is not None:
            if (VIDs[i] == 1027) & (PIDs[i] == 24577):
                 #Sets the 'target' port as the one associated with these matching IDs
                PROSIM.port = com_ports[i]
                print("Fluke Pro Sim 8 found at:",PROSIM.port, "\n")
                return PROSIM.port
        elif(i == [len(VIDs)-1 or len(PIDs)-1]):   #When at end of list of COM ports.
            print("No Device Found.\n")
        else:
            continue


PATHcheck("/Users/Alex.Ngan/OneDrive - Zoll Medical Corporation (1)/Documents/sturdy-waffle/")
NewCase()
print("Target:", AutoFind())
print("Serial ports:", com_ports)
PROSIM.open() #need to check if target exists, then try this
print(PROSIM.write(b"SN"))
#print("reply:", (PROSIM.readline()).decode())