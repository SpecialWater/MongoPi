#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 20:11:43 2019

@author: pi
"""

import os
import sqlite3
import requests

def postRPi(http, json_var):
    res = requests.post(http, json=json_var)
    return res.status_code

def db_connect(db_name, timeout):
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), db_name)
    con = sqlite3.connect(DEFAULT_PATH, timeout=timeout)
    return con

def formatResult(cur, tableName):
    cur.execute("SELECT * FROM %s" % tableName)
    selectString = cur.fetchall()
    formated = [f"{id:<5}{time_record:<35}{temp:<15}{humid:<15}" for id, time_record, temp, humid in selectString]
    id, time_record, temp, humid = "PID", "TimeStamp", "Temperature", "Humidity"
    print('\n'.join([f"{id:<5}{time_record:<35}{temp:<15}{humid:<15}"] + formated))
    

def insertSQL(con, cur, tableName, uid, timestamp, temp, humid):
    sql = "INSERT INTO %s (id, time_record, temp, humid) VALUES (?, ?, ?, ?)" %tableName
    cur.execute(sql, (uid, timestamp, temp, humid))
    con.commit()