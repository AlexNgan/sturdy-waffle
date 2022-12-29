import inspect
import subprocess
import sys
import serial
import serial.tools.list_ports as ports
from serial.tools.list_ports import comports
import time

#Creates output txt file, need to write in code to capture user input for participant number
def GenerateReport(): 
    with open('output' + VARIABLE + '.txt', 'w') as f:
        out = subprocess.run('ping 127.0.0.1', shell=True, stdout=f, text=True)