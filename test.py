#Fluke hardware ID: FTDIBUS\COMPORT&VID_0403&PID_6001
'''
Some commands are designed to pass from the ProSim 8 directly to the plugged in SpO2 or other Auxiliary device. These commands are prefixed with @. Then the command, with the @ removed is passed through to the Auxiliary port.
'''
#FLUKE 2: PID (24577), VID (1027)
#import prosim8.ecg
import inspect
import subprocess
import sys
import serial
import serial.tools.list_ports as ports
from serial.tools.list_ports import comports 
#import prosim8
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

ProSim = PROSIM

def NewCase():
    subprocess.run("cls", shell=True, check=True) #Clears the shell.


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
    ProSim.spo2.set_spo2_sat(94) # sets SpO2 to 94%
    ProSim.spo2.sat()            # sets SpO2 to 94%

NewCase()
print("Target:", AutoFind())
print("Serial ports:", com_ports)
#OpenSesame()
PROSIM.open() #need to check if target exists, then try this
print(PROSIM.write(b"SN"))
#print("reply:", (PROSIM.readline()).decode())