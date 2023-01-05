#Fluke hardware ID: FTDIBUS\COMPORT&VID_0403&PID_6001
'''
Some commands are designed to pass from the ProSim 8 directly to the plugged in SpO2 or other Auxiliary device. These commands are prefixed with @. Then the command, with the @ removed is passed through to the Auxiliary port.
'''
#FLUKE 2: PID (24577), VID (1027)

import inspect
import subprocess
import sys
import serial
import serial.tools.list_ports as ports
from serial.tools.list_ports import comports 
import prosim8
from prosim8.prosim import PROSIM
import time

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

com_ports = [i.device for i in ports.comports()]
#com_ports = [str(i) for i in ports.comports()]# create a list of ['COM1','COM2'] as str
PIDs = [i.pid for i in ports.comports()] #List of product IDs (integers unless 'None')
VIDs = [i.vid for i in ports.comports()] #List of vendor IDs (integers unless 'None')

def NewCase():
    subprocess.run("cls", shell=True, check=True) #Clears the shell.
    
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

#Debug function in case the port auto-select fails.
def ScanPorts(): 
    sys.stderr.write('\n--- Available ports:\n')
    # for i in com_ports:
    #     print(com_ports, "\n")
    for i, (name, vid, pid) in enumerate(sorted(comports()), 1):             
       sys.stderr.write('--- {:2}: {:20} {}\n'.format(name, vid, pid))

    global PROSIM
    PROSIM.port = input('--- Enter port index or full name: ')
    try:
        index = int(PROSIM.port) - 1 #THIS WILL NOT WORK, FIX TOMORROW...SELECTED PORT IS A LITERAL AND I NEED TO MAKE THE USER INPUT PART MAP COM PORT NAMES TO OPTIONS 1, 2, 3, ETC.
        if not 0 <= index < len(com_ports):
            sys.stderr.write('--- Invalid index!\n')        
    except ValueError:
        pass        
    else:
        PROSIM.port = com_ports[index]

#Takes the target serial port as an argument.
def OpenSesame():
    global PROSIM 
    try:
        PROSIM.close()
        PROSIM.open()
    except:
        pass
    return PROSIM
# try:
#     PROSIM = serial.Serial(
#         port=selected_port,
#         baudrate=115200,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE,
#         bytesize=serial.EIGHTBITS,
#         xonxoff=False,
#         timeout=0.5,
#         write_timeout=0.5
#     )
    
# except:
#     pass

def sat(self):
        sat = ""
        return self.device.send('SN%s' % sat)

NewCase()
print("Target:", AutoFind())
print("Serial ports:", com_ports)
#OpenSesame()
PROSIM.open() #need to check if target exists, then try this
#print(PROSIM)
#print(PROSIM.write(b"SN"))
print("reply:", (PROSIM.readline()).decode())