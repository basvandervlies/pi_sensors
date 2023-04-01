#!/usr/bin/python

import HPMA115S0
import time
import os
import sys
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

hpma115S0 = HPMA115S0.HPMA115S0("/dev/serial0")
hpma115S0.init()
hpma115S0.startParticleMeasurement()
hpma115S0.readParticleMeasurement()


x_data = []
pm2_data = [] 
pm10_data = []
pm2_max = [ ]

while 1:
	if (hpma115S0.readParticleMeasurement()):
    		t = datetime.now()
   		print("PM2.5:%d ug/m3" %(hpma115S0._pm2_5))
   		print("PM10:%d ug/m3" %(hpma115S0._pm10))
    		x_data.append(t)
        	pm2_data.append(hpma115S0._pm2_5) 
        	pm2_max.append("20") 
        	pm10_data.append(hpma115S0._pm10) 
		break
	else:
		print("Device not ready yet, sleeping 1 sec")
		time.sleep(1)


#figure = pyplot.figure()
#figure.suptitle("STEBETO Stof meter", fontsize='14', fontweight='14')

figure,ax = pyplot.subplots()

line_pm2, = pyplot.plot_date(x_data, pm2_data, ls='solid', color='blue', label='pm2.5')
line_pm2_max, = pyplot.plot_date(x_data, pm2_max, ls='solid', color='red', label='pm2.5 European norm')
line_pm10, = pyplot.plot_date(x_data, pm10_data, ls='solid', color="gray", label="pm10")

ax.set(xlabel="time", ylabel="fijnstof ug/m3", title="STEBETO fijnstof meter")
ax.legend(loc='upper left')
ax.grid(True)

f = open("data.txt", "w")
f.write("time, pm2.5, pm10\n")

def update(frame):
    t = datetime.now()
    global pm2_data
    global x_data 
    global pm2_max 
    global pm10_data
  
    x_data.append(t)
    if (hpma115S0.readParticleMeasurement()):
        print("PM2.5 %s:%d ug/m3" %(str(t),hpma115S0._pm2_5))
        print("PM10 %s:%d ug/m3" %(str(t),hpma115S0._pm10))
        f.write("%s,%d,%d\n" %(t, hpma115S0._pm2_5, hpma115S0._pm10))

    pm2_data.append(hpma115S0._pm2_5) 
    pm2_max.append("20") 
    pm10_data.append(hpma115S0._pm10) 

    line_pm2.set_data(x_data, pm2_data)
    line_pm2_max.set_data(x_data, pm2_max)
    line_pm10.set_data(x_data, pm10_data)

    return pm2_data

    #figure.gca().relim()
    #figure.gca().autoscale_view()


animation = FuncAnimation(figure, update, interval=5000)
pyplot.show()
f.close()
