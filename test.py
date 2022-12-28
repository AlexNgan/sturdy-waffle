#Fluke hardware ID: FTDIBUS\COMPORT&VID_0403&PID_6001

#FLUKE 2: PID (24577), VID (1027)

import inspect
import subprocess
import sys
import serial
import serial.tools.list_ports as ports
from serial.tools.list_ports import comports 

com_ports = [str(i) for i in ports.comports()]# create a list of ['COM1','COM2'] as str
PIDs = [i.pid for i in ports.comports()] #List of integers unless None
VIDs = [i.vid for i in ports.comports()] 
desc = [i.name for i in ports.comports()] 

selected_port = ''  #To hold name of port that matches user input.

try:
    ser = serial.Serial(
        port= selected_port,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        xonxoff=True
    )
    ser.isOpen()
except:
    print("nothing in COM6")


#Clears the shell.
def NewCase():
    subprocess.run("cls", shell=True, check=True)

#Debug function in case the port auto-select fails.
def ScanPorts(): 
    sys.stderr.write('\n--- Available ports:\n')
    # for i in com_ports:
    #     print(com_ports, "\n")
    for i, (name, vid, pid) in enumerate(sorted(comports()), 1):             
       sys.stderr.write('--- {:2}: {:20} {}\n'.format(name, vid, pid))

    selected_port = input('--- Enter port index or full name: ')
    try:
        index = int(selected_port) - 1 #THIS WILL NOT WORK, FIX TOMORROW...SELECTED PORT IS A LITERAL AND I NEED TO MAKE THE USER INPUT PART MAP COM PORT NAMES TO OPTIONS 1, 2, 3, ETC.
        if not 0 <= index < len(com_ports):
            sys.stderr.write('--- Invalid index!\n')        
    except ValueError:
        pass        
    else:
        selected_port = com_ports[index]

#Function to autodetect and connect to first COM port that has FTDI as manufacturer.
def AutoFind():  
    for i in range(len(com_ports)): 
        if VIDs[i] is not None:
            if (VIDs[i] == 1027) & (PIDs[i] == 24577):
                print("Fluke Pro Sim 8 found.\n")
                break
        elif(i == [len(VIDs)-1 or len(PIDs)-1]):   #When at end of list of COM ports.
            print("No Device Found.\n")
        else:
            continue

#Creates output txt file, need to write in code 
#to capture user input for participant number
#def GenerateReport(): 
    #with open('output' + VARIABLE + '.txt', 'w') as f:
        #out = subprocess.run('ping 127.0.0.1', shell=True, stdout=f, text=True)
NewCase()
AutoFind()