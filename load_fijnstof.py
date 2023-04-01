#!/usr/bin/python

import time
import os
import sys
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.dates as mdates

#data = np.loadtxt("data.txt", delimiter=',',skiprows=1, names=["t", "p2_5", "p10"])
t_data,pm2_5_data,pm10_data = np.loadtxt("data.txt", 
 delimiter=',',
 skiprows=1, 
 unpack=True,
 converters = {0: mdates.strpdate2num("%Y-%m-%d %H:%M:%S.%f")})



figure,ax = pyplot.subplots()

line_pm2, = pyplot.plot_date(t_data, pm2_5_data, ls='solid', color='blue', label='pm2.5')
#line_pm2_max, = pyplot.plot_date(x_data, pm2_max, ls='solid', color='red', label='pm2.5 European norm')
line_pm10, = pyplot.plot_date(t_data, pm10_data, ls='solid', color="gray", label="pm10")


ax.set(xlabel="time", ylabel="fijnstof ug/m3", title="STEBETO fijnstof meter")
ax.legend(loc='upper left')
ax.grid(True)

figure.gca().relim()
figure.gca().autoscale_view()

pyplot.show()
