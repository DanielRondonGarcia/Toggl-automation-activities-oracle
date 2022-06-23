#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author DanielRondonGarcia <daniel5232010@gmail.com>

from typing_extensions import Self
from unittest import result
import requests
from requests.structures import CaseInsensitiveDict
import json  # parsing json data
from bs4 import BeautifulSoup
from base64 import b64encode
from datetime import datetime,timedelta
from dateutil.parser import parse
import re
import sys
import pprint
import consultas
import config
import math

Null = None
flag = False
now = datetime.now()
# template of headers for our request
headers = {
    "Authorization": "",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "User-Agent": "python/urllib",
}
def internet_on():
    """Checks if internet connection is on by connecting to Google"""
    try:
        requests.get('http://www.google.com', timeout=10)
        return True
    except requests.exceptions.ConnectionError:
        return False
    except:
        return False
# ------------------------------------------------------------
# Métodos auxiliares
# ------------------------------------------------------------
def progress_bar(progress,total):
    percent=100*(progress/float(total))
    bar='█'* int(percent)+'-'*(100 - int(percent))
    print(f"\r{bar}|{percent:.2f}%",end="\r")

def saveJson(data):
    with open('logs/data-'+str(now.strftime('%d-%m-%Y'))+'.json', 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

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
    pattern = '(ACT\[[0-9]*\-)'
    lista = re.search(pattern,str)
    limpieza = lista[1]
    limpieza = re.sub("ACT\[","",limpieza)
    return re.sub("\-","",limpieza)

def cleanAct(str):
    pattern = '(-[0-9]{2}\])'
    lista = re.search(pattern,str)
    limpieza = lista[1]
    limpieza = re.sub("\-","",limpieza)
    return re.sub("\]","",limpieza)

def cleanDescription(str):
    pattern = "(?<=\]-).*(?=.*)"
    lista = re.search(pattern,str)
    limpieza = lista[0]    
    return limpieza
    
# ------------------------------------------------------------
# Métodos que modifican los encabezados para controlar nuestras solicitudes HTTP
# ------------------------------------------------------------
def setAPIKey(APIKey):
    '''establecer la clave API en el encabezado de la solicitud'''
    # elaborar la Autorización
    authHeader = APIKey + ":" + "api_token"
    authHeader = "Basic " + b64encode(authHeader.encode()).decode('ascii').rstrip()

    # add it into the header
    headers['Authorization'] = authHeader

setAPIKey(config.apiKey)

    # -----------------------------------------------------
    # Métodos para solicitar datos directamente desde un punto final
    # -----------------------------------------------------

def requestApi(url):
    url_result = requests.get(url, headers=headers)
    soup = BeautifulSoup(url_result.content, 'html.parser')
    site_json=json.loads(soup.text)
    return site_json

    # -----------------------------------------------------
    # Insertar los datos a la base de datos
    # -----------------------------------------------------
def main():
    print("Hola")
    print("Comprobando la conectividad a Internet...")
    if not internet_on():
        print("OMG! ¡No hay conexión a Internet!")
        print("¡Adiós mundo cruel!")
        sys.exit()    
    print("¡Internet parece estar bien!")
    print("\nIntentando conectarme a Toggl, ¡espera!\n")
    try:
        response = requestApi("https://api.track.toggl.com/api/v9/me")
        print("Client name: %s  Client ID: %s" % (response['fullname'], response['id']))
        flag = True
    except:
        print("OMG! ¡La solicitud de alternar falló por alguna razón misteriosa!")
        print("¡Adiós mundo cruel!")
        sys.exit()

    if flag:
        time_entries = requestApi("https://api.track.toggl.com/api/v9/me/time_entries")
        sum_time=0
        data = {}
        data['entradas'] = []
        for time_entrie in time_entries:
            start = re.sub("\+00:00","",time_entrie['start'])
            start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
            if start > now-timedelta(days=1): #Condición para que solo muestre los del día de hoy
                print(time_entrie['description'])
                RQ = cleanRq(time_entrie['description'])
                etapa = cleanEtapa(time_entrie['description'])
                act = cleanAct(time_entrie['description'])
                description = cleanDescription(time_entrie['description'])
                print(RQ)
                print(etapa)
                print(act)
                print(description)
                print(start)    
                if time_entrie['stop'] != Null:
                    stop = datetime.strptime(time_entrie['stop'], '%Y-%m-%dT%H:%M:%SZ')
                    print(stop)
                    diff=stop-start
                    hours=timeMinuteToHour(diff)
                    sum_time=sum_time+hours
                    print("Diff: %s  Diff in Hours: %s" % (diff, hours))
                    data['entradas'].append({
                    'rq': RQ,
                    'etapa': etapa,
                    'act': act,
                    'description': description,
                    'diff': hours,
                    'Total': sum_time})
                print("\n")
            print("Total Hours: %s" % (round(sum_time,1)))
            saveJson(data)
            pprint.pp(data)
            consultas.inserInto(data)            

if __name__ == '__main__':
    main()