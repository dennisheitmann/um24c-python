#!/usr/bin/python3

import serial
import time
import datetime
import sys

try:
    rfcomm = serial.Serial(port = serial_port, baudrate = 9600, timeout = 1)
    rfcomm.flushInput()
except:
    print(serial_port, "not available")
    exit(1)

sleeptime = 2.5

print("#record steps: "+str(sleeptime)+"s")
print("#Datetime; Voltage [V]; Current [A]; Power [W]; Temperature [C]")

while True:
    rfcomm.write(bytes([0xf0]))
    s = rfcomm.read(130)
    if (sys.getsizeof(s) < 130): continue
    voltage = int((ord(chr(s[2])) <<8)| ord(chr(s[3]))) 
    if (voltage < 2): continue
    current = int((ord(chr(s[4])) <<8)| ord(chr(s[5])))
    power = int((ord(chr(s[6])) <<24)| (ord(chr(s[7])) <<16)| (ord(chr(s[8])) <<8)|ord(chr(s[9])))
    tempC = int((ord(chr(s[10])) <<8)| ord(chr(s[11]))) 
    print('"'+str(datetime.datetime.now())+'"'+";"+'"'+str(voltage/100.0)+'"'+";"+'"'+str(current/1000.0)+'"'+";"+'"'+str(power/1000.0)+'"'+";"+'"'+str(tempC)+'"'+';')
    sys.stdout.flush()
    time.sleep(sleeptime)
rfcomm.close()
