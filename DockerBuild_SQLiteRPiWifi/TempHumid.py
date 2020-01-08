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
from db_utils import insertSQL
from db_utils import db_connect
from datetime import datetime
import sqlite3

# Connect to database
con = db_connect('SensorRead.db', timeout = 10)
cur = con.cursor()

# Create table
currtime = datetime.now()
currtime = currtime.strftime("%Y_%m_%d_%H_%M_%S")

tableName = "TempHumid" + currtime
table_sql = """
CREATE TABLE %s (
        id integer,
        time_record datetime,
        temp integer,
        humid integer)""" % tableName
        
cur.execute(table_sql)

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

PriorFailure = False

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
    
    # Check if the write to RPi failed and if so, store locally
    if(check1 != 200 or check2 != 200):
        # Insert readings into sqlLite db
        insertSQL(con, cur, tableName, 1, datetime.now(), temperature, humidity)
        PriorFailure = True
        print('Writing to SQL')
    else:
        print('Writinng to Server, temp: ' + str(temperature) + ' , humidity: ' + str(humidity))
    
    # If there is local storage and connection has been re-established
    if PriorFailure and (check1 == 200 and check2 == 200):
        PriorFailure = False
        print('Reading from SQL into Server')
        # Get local storage and loop through to write back to server
        cur.execute("SELECT * FROM %s" % tableName)
        selectString = cur.fetchall()
        for row in selectString:
            json_var_temp = {'source': 'Andrew',
                             'variable': 'temperature',
                             'value': row[2]}
            json_var_humidity = {'source': 'Andrew',
                             'variable': 'temperature',
                             'value': row[3]}
            check1 = postRPi(http, json_var=json.dumps(json_var_temp))
            check2 = postRPi(http, json_var=json.dumps(json_var_humidity))
        
        # Remove local storage thas has been written back
        cur.execute("DELETE FROM %s" % tableName)
        print('done')
        
    lcd.show_cursor(False)
    lcd.set_cursor(0,0)
    lcd.message("Temp: %d F \n" % temperature)
    lcd.message("Humidity: %d %%" % humidity)
    
# docker run --privileged -v /home/pi/PythonScripts/MongoPi/DockerBuild:/data  temphumid