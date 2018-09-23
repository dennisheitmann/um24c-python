#!/usr/bin/python3

import tkinter
import serial
import time
import datetime
import sys
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')

rfcomm = serial.Serial(port = "/dev/rfcomm1", baudrate = 9600, timeout = 1)
rfcomm.flushInput()

sleeptime = 2.5

top = tkinter.Tk()
frame = tkinter.Frame(top)
frame.pack()
bottomframe = tkinter.Frame(top)
bottomframe.pack(side = tkinter.BOTTOM)

date_gui = str(datetime.datetime.now())
voltage_gui = str("0.000 V")
current_gui = str("0.000 A")
power_gui = str("0.000 W")
temp_gui = str("0 C")

label_d = tkinter.Label(frame, text = date_gui, relief = tkinter.RAISED)
label_v = tkinter.Label(frame, text = voltage_gui, relief = tkinter.RAISED)
label_c = tkinter.Label(frame, text = current_gui, relief = tkinter.RAISED)
label_p = tkinter.Label(frame, text = power_gui, relief = tkinter.RAISED)
label_t = tkinter.Label(frame, text = temp_gui, relief = tkinter.RAISED)
label_d.pack(side = tkinter.TOP)
label_v.pack(side = tkinter.LEFT)
label_c.pack(side = tkinter.LEFT)
label_p.pack(side = tkinter.LEFT)
label_t.pack(side = tkinter.LEFT)
fig = Figure(figsize=(5,4), dpi = 100)
a = fig.add_subplot(111)
a.xaxis.set_tick_params(rotation=30)
canvas = FigureCanvasTkAgg(fig, master = bottomframe)
canvas.show()
canvas.get_tk_widget().pack(side = 'right', fill = 'both', expand = 1, ipadx = 50, ipady = 50)
dates = []
powers = []

def SerialRun(event = None):
    rfcomm.write(bytes([0xf0]))
    s = rfcomm.read(130)
    if (sys.getsizeof(s) < 130):
        top.after(1000, SerialRun)
        return
    voltage = int((ord(chr(s[2])) <<8)| ord(chr(s[3]))) 
    if (voltage < 2):
        top.after(1000, SerialRun)
        return
    current = int((ord(chr(s[4])) <<8)| ord(chr(s[5])))
    power = int((ord(chr(s[6])) <<24)| (ord(chr(s[7])) <<16)| (ord(chr(s[8])) <<8)|ord(chr(s[9])))
    tempC = int((ord(chr(s[10])) <<8)| ord(chr(s[11]))) 
    print('"'+str(datetime.datetime.now())+'"'+";"+'"'+str(voltage/100.0)+'"'+";"+'"'+str(current/1000.0)+'"'+";"+'"'+str(power/1000.0)+'"'+";"+'"'+str(tempC)+'"'+';')
    date_gui = (str(datetime.datetime.now()))
    voltage_gui = (str(voltage/100.0))
    current_gui = (str(current/1000.0))
    power_gui = (str(power/1000.0))
    temp_gui = (str(tempC))
    dates.append(datetime.datetime.now())
    powers.append(power)
    a.clear()
    a.xaxis.set_tick_params(rotation=30)
    a.margins(0.5)
    a.plot_date(dates, powers)
    canvas.draw()
    label_d.config(text = date_gui)
    label_v.config(text = voltage_gui+" V")
    label_c.config(text = current_gui+" A")
    label_p.config(text = power_gui+" W")
    label_t.config(text = temp_gui+" C")
    sys.stdout.flush()
    top.update()
    top.after(5000, SerialRun)

top.after(5000, SerialRun)
top.mainloop()
rfcomm.close()
