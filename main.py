#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author DanielRondonGarcia <daniel5232010@gmail.com>

import os
import sys
from typing_extensions import Self
import config
import requests
from requests.structures import CaseInsensitiveDict
import json  # parsing json data
import math
import sys
import time
from bs4 import BeautifulSoup
from base64 import b64encode
from datetime import datetime,timedelta
from base64 import b64encode
from dateutil.parser import parse
import re

Null = None
# template of headers for our request
headers = {
    "Authorization": "",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "User-Agent": "python/urllib",
}

# default API user agent value
user_agent = "TogglPy"
# ------------------------------------------------------------
# Auxiliary methods
# ------------------------------------------------------------
def timeMinuteToHour(time):
    return round(time/timedelta(hours=1), 1)

def decodeJSON(jsonString):
    return json.JSONDecoder().decode(jsonString)
def cleanRq(str):
    pattern = '(RQ\[[0-9]*\])'
    lista = re.search(pattern,str)
    limpieza = lista[1]
    limpieza = re.sub("RQ\[","",limpieza)
    return re.sub("\]","",limpieza)
def cleanEtapa(str):
    pattern = '(RQ\[[0-9]*\])'
    lista = re.search(pattern,str)
    limpieza = lista[1]
    limpieza = re.sub("RQ\[","",limpieza)
    return re.sub("\]","",limpieza)
    
# ------------------------------------------------------------
# Methods that modify the headers to control our HTTP requests
# ------------------------------------------------------------
def setAPIKey(APIKey):
    '''set the API key in the request header'''
    # craft the Authorization
    authHeader = APIKey + ":" + "api_token"
    authHeader = "Basic " + b64encode(authHeader.encode()).decode('ascii').rstrip()
    print(authHeader)

    # add it into the header
    headers['Authorization'] = authHeader

setAPIKey("5618cca12fe41c7d6740979af73aa7c3")

    # -----------------------------------------------------
    # Methods for directly requesting data from an endpoint
    # -----------------------------------------------------

def requestApi(url):
    url_result = requests.get(url, headers=headers)
    soup = BeautifulSoup(url_result.content, 'html.parser')
    site_json=json.loads(soup.text)
    return site_json

response = requestApi("https://api.track.toggl.com/api/v9/me")

print("Client name: %s  Client ID: %s" % (response['fullname'], response['id']))


response1 = requestApi("https://api.track.toggl.com/api/v9/me/time_entries")

year = datetime.now().year
month = datetime.now().month
day = datetime.now().day
hour = datetime.now().hour
timestruct = datetime(year, month, day, hour).isoformat()
print(timestruct)

sum_time=0
for time_entries in response1:
    print(time_entries['description'])
    RQ = cleanRq(time_entries['description'])
    print(RQ)
    start = re.sub("\+00:00","",time_entries['start'])
    start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
    print(start)
    if time_entries['stop'] != Null:
        stop = datetime.strptime(time_entries['stop'], '%Y-%m-%dT%H:%M:%SZ')
        print(stop)
        diff=stop-start
        hours=timeMinuteToHour(diff)
        sum_time=sum_time+hours
        print("Diff: %s  Diff in Hours: %s" % (diff, hours))
    print("\n")
print("Total Hours: %s" % (round(sum_time,1)))
