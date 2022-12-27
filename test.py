#Fluke hardware ID: FTDIBUS\COMPORT&VID_0403&PID_6001

#Try to import pyserial modules.
import subprocess
import sys
import serial.tools.list_ports as ports
from serial.tools.list_ports import comports 

com_ports = list(ports.comports()) # create a list of com ['COM1','COM2']
selected_port = ""  #Hold name of port that matches

#Clears the shell.
def NewCase():
    subprocess.run("cls", shell=True, check=True)

#Debug function in case the port auto-select fails.
def ScanPorts(): 
    sys.stderr.write('\n--- Available ports:\n')
    for n in com_ports:
        sys.stderr.write(com_ports[n], "\n")
    #for n, (port, device, product), in enumerate(sorted(com_ports), 1):             
      #  sys.stderr.write('--- {:2}: {:20} {}\n'.format(port, device, product))

    port = input('--- Enter port index or full name: ')
    try:
        index = int(port) - 1
        if not 0 <= index < len(com_ports):
            sys.stderr.write('--- Invalid index!\n')        
    except ValueError:
        pass        
    else:
        port = com_ports[index]

#Function to autodetect and connect to first COM port that has FTDI as manufacturer.
def AutoFind(manufacture_name):  
    for p in com_ports:
        if p.manufacturer is not None:
            #Casefold to ignore case for input vs. device info.
            if p.manufacturer.casefold() == manufacture_name.casefold():
                print(manufacture_name,"connected.\n")
                break
            elif(p == com_ports[(len(com_ports)-1)]):   #When at end of list of COM ports.
                print("No", manufacture_name, "Device Found.\n")
            else:
                continue
        else:
            continue

#Creates output txt file, need to write in code 
#to capture user input for participant number
#def GenerateReport(): 
    #with open('output' + VARIABLE + '.txt', 'w') as f:
        #out = subprocess.run('ping 127.0.0.1', shell=True, stdout=f, text=True)
ScanPorts()
#AutoFind("FTDI")