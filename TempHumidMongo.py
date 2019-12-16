#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 14:48:44 2019

@author: pi
"""

#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi
import Adafruit_CharLCD as LCD
import Adafruit_DHT
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pymongo import MongoClient

# Raspberry Pi pin setup
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)


# Parameters
x_len = 100         # Number of points to display
y_range = [20, 100]  # Range of possible Y values to display

# Create figure for plotting
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
xs1 = list(range(0, x_len))
ys1 = [0] * x_len
xs2 = list(range(0, x_len))
ys2 = [0] * x_len
ax1.set_ylim(y_range)
ax2.set_ylim(y_range)

# Create a blank line. We will update the line in animate
line1, = ax1.plot(xs1, ys1)
line2, = ax2.plot(xs2, ys2)

# Add labels
plt.title('Temp / Humidity over Time')
plt.xlabel('Samples')
ax1.set_title('Temp')
ax2.set_title('Humidity')
ax1.set_ylabel('Temperature (deg F)')
ax2.set_ylabel('Humidity (%)')

plt.subplots_adjust(hspace=.6)

# This function is called periodically from FuncAnimation
def animate(i, ys1, ys2):

    # Read temperature (Celsius) from TMP102
    humidity, temperature = Adafruit_DHT.read_retry(11, 4, delay_seconds=.1)
    temperature = temperature * 9 / 5 + 32
    
    lcd.show_cursor(False)
    lcd.set_cursor(0,0)
    lcd.message("Temp: %d F \n" % temperature)
    lcd.message("Humidity: %d %%" % humidity)
    
    # Add y to list
    ys1.append(temperature)
    ys2.append(humidity)

    # Limit y list to set number of items
    ys1 = ys1[-x_len:]
    ys2 = ys2[-x_len:]

    # Update line with new Y values
    line1.set_ydata(ys1)
    line2.set_ydata(ys2)

    return line1, line2

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys1,ys2),
    interval=100,
    blit=True)
plt.show()

    
    



