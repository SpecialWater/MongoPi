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
import json
from db_utils import postRPi

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

# Connect to RPi Server
http = 'http://10.166.45.219:5000/collect'

while True:

    # Read temperature (Celsius) from TMP102
    humidity, temperature = Adafruit_DHT.read_retry(11, 4, delay_seconds=.1)
    temperature = temperature * 9 / 5 + 32
    
    json_var_temp = {
            'source': 'Andrew',
            'variable': 'temperature',
            'value': temperature}
    json_var_humidity = {
            "source": "Andrew",
            "variable": "humidity",
            "value": humidity}
    
    # Insert readings into sqlLite db
    check1 = postRPi(http, json_var=json.dumps(json_var_temp))
    check2 = postRPi(http, json_var=json.dumps(json_var_humidity))
    
    print(check1, check2)
    
    lcd.show_cursor(False)
    lcd.set_cursor(0,0)
    lcd.message("Temp: %d F \n" % temperature)
    lcd.message("Humidity: %d %%" % humidity)
    
