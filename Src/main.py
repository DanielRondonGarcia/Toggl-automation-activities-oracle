#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author DanielRondonGarcia <daniel5232010@gmail.com>

from unittest import result
from click import confirm
import requests
from requests.structures import CaseInsensitiveDict
import json  # parsing json data
from bs4 import BeautifulSoup
from base64 import b64encode
from datetime import datetime,timedelta
from dateutil.parser import parse
import re
import sys
import time
import consultas
import config
import math
import arrow

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

def saveJson(data, date):
    print(date)
    with open('logs/data-'+str(date.strftime('%d-%m-%y'))+'.json', 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

def SecondsToHours(time):
    return round(time/3600, 1)

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
    pattern = '(-[0-9]{1,3}\])'
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
    print(authHeader)

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
        print("Escribe la fecha a registrar con el formato YYYY/MM/DD")
        fechaVal = input()
        date_to_compare = datetime.strptime(fechaVal, "%Y/%m/%d")
        print(f"Fecha: {date_to_compare}")
        for time_entrie in time_entries:
            start = arrow.get(time_entrie['start']).to(config.timeZone)
            if start.date() == date_to_compare.date(): #Condición para que solo muestre las entradas del 23
                RQ = cleanRq(time_entrie['description'])
                etapa = cleanEtapa(time_entrie['description'])
                act = cleanAct(time_entrie['description'])
                description = cleanDescription(time_entrie['description'])
                print("==========================================================================")
                print("Requerimiento: "+str(RQ))
                print("Etapa: "+str(etapa))
                print("Actividad: "+str(act))
                print("Descripción: "+description)
                print("Fecha de incio: "+str(start))                
                if time_entrie['stop'] != Null:
                    diff=time_entrie["duration"];
                    hours=SecondsToHours(diff)
                    sum_time=sum_time+hours
                    print("Diff: %s  Diff in Hours: %s" % (diff, hours))
                    data['entradas'].append({
                    'rq': RQ,
                    'etapa': etapa,
                    'act': act,
                    'description': description,
                    'diff': hours,
                    'Total': sum_time})
                print("==========================================================================")
                print("\n")
        print("Total Hours: %s" % (round(sum_time,1)))
        saveJson(data,date_to_compare)
        print("Escribe el Numero 1 si quiere registrar el tiempo en el SGI, si no, solo oprima la tecla Enter. Tambien puedes ver mejor cada detalle en el archivo creado en la ruta: "+'logs/data-'+str(date_to_compare.strftime('%d-%m-%Y'))+'.json')
        confirm = input()
        print(f"Escribió: {confirm}")
        try:
            if int(confirm) == 1:
                """ pprint.pp(data) """
                consultas.inserInto(data,date_to_compare)
        except Exception as e:
            print("No se han guardado las actividades")
            print("Error: ", e)
            print("Esperando 10 segundos...")
            time.sleep(10)
            sys.exit()

if __name__ == '__main__':
    main()
    print("Esperando 10 segundos...")
    time.sleep(10)
    sys.exit()
