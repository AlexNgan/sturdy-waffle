#!/usr/bin/env python3

#The main code will live here, functions will be mapped to keys
import prosim8 
import serial
import serial.tools.list_ports as ports
from serial.tools.list_ports import comports 
import subprocess
import sys

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

GetModules()