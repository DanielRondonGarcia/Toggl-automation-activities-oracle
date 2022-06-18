from bs4 import BeautifulSoup
import requests
""" import api_telegram """
from requests.structures import CaseInsensitiveDict
import json
from datetime import datetime,timedelta
def IsoToDateTime(fecha):
    return datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S.%fZ")
Null = None
def timedelta_hour_to_minute(time):
    return int(float(time.replace('Horas',''))*60)
def request_api(bearer):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer "+bearer
    url_result = requests.get('https://backend-farm.plantvsundead.com/farms?limit=10&offset=0', headers=headers)
    soup = BeautifulSoup(url_result.content, 'html.parser')
    site_json=json.loads(soup.text)
    return site_json

def messsage_info(bearer):    
    bandera_time_water_minutes = False
    cont = 0
    cont2=0
    data_plants = {}
    data_print = []
    data_plants['planta'] = []
    for data_data in request_api(bearer)['data']:
        try:
            cuervo = data_data['pausedTime']
        except KeyError:
            cuervo = None
        try:
            time_water = (IsoToDateTime(data_data['activeTools'][1]['endTime'])-datetime.utcnow())/timedelta(hours=1)
            time_water = round(time_water , 3)
            time_water = str(time_water)+' Horas'
        except IndexError:
            time_water = '0'
        try:
            dead_matera = (IsoToDateTime(data_data['activeTools'][0]['endTime'])-datetime.utcnow())/timedelta(hours=1)
            dead_matera = round(dead_matera, 1)
            dead_matera = str(dead_matera)+' Horas'
        except IndexError:
            dead_matera = '0'
        try:
            tiempo_cosecha = (IsoToDateTime(data_data['harvestTime'])-datetime.utcnow())/timedelta(hours=1)
            tiempo_cosecha = round(tiempo_cosecha, 2)
            tiempo_cosecha = str(tiempo_cosecha)+' Horas'
        except IndexError:
            tiempo_cosecha = '0'

        data_plants['planta'].append({
            'tipo':data_data['plant']['iconUrl'],
            'tiempo_cosecha':tiempo_cosecha,
            'dead_matera': dead_matera,
            'time_water': time_water,
            'need_wather': data_data['needWater'],
            'cuervo': cuervo,
        })    
    for planta in data_plants['planta']:
        time_water_minutes = timedelta_hour_to_minute(planta['time_water'])
        if time_water_minutes == 2 or time_water_minutes == 1:
            bandera_time_water_minutes=True    
        else:
            bandera_time_water_minutes=False     
        if planta['cuervo'] != None: 
            alerta = f"🦅 ¡ATENCIÓN! una planta tiene un cuervo hace: {str(datetime.utcnow()-IsoToDateTime(planta['cuervo']))}\nApurate\nhttps://marketplace.plantvsundead.com/farm#/farm"
            data_print.append(alerta)
        if planta['need_wather'] != False: 
            cont2+=1
            alerta = f" 💦💦¡{cont2}  ATENCIÓN! PLANTA SIN AGUA URGENTE\nApurate\nhttps://marketplace.plantvsundead.com/farm#/farm\nTipo {planta['tipo']}"
            data_print.append(alerta)
        if timedelta_hour_to_minute(planta['tiempo_cosecha']) <= 2: 
            alerta = f" 🌿¡ATENCIÓN! Tiempo de cosechar\nApurate\nhttps://marketplace.plantvsundead.com/farm#/farm\nTipo {planta['tipo']}"
            data_print.append(alerta)
        if bandera_time_water_minutes == True:
            alerta = f" ⏱¡ATENCIÓN! una planta necesitará agua en: {str(time_water_minutes)} minutos\nApurate y ve a regarlas\nhttps://marketplace.plantvsundead.com/farm#/farm\nTipo {planta['tipo']}"
            data_print.append(alerta)
    print('Working info')
    """ print(data_print) """
    return(data_print)


def messsage_info_general(bearer):
    data_plants = {}
    data_plants['planta'] = []
    texto =''
    cont_plant = 0
    for data_data in request_api(bearer)['data']:
        try:
            cuervo = data_data['pausedTime']
        except KeyError:
            cuervo = None
        try:            
            time_water = (IsoToDateTime(data_data['activeTools'][1]['endTime'])-datetime.utcnow())/timedelta(hours=1)
            time_water = round(time_water , 3)
            time_water = str(time_water)+' Horas'
        except IndexError:
            time_water = '0'
        try:            
            dead_matera = (IsoToDateTime(data_data['activeTools'][0]['endTime'])-datetime.utcnow())/timedelta(hours=1)
            dead_matera = round(dead_matera, 1)
            dead_matera = str(dead_matera)+' Horas'
        except IndexError:
            dead_matera = '0'
        try:            
            tiempo_cosecha = (IsoToDateTime(data_data['harvestTime'])-datetime.utcnow())/timedelta(hours=1)
            tiempo_cosecha = round(tiempo_cosecha, 2)
            tiempo_cosecha = str(tiempo_cosecha)+' Horas'
        except IndexError:
            tiempo_cosecha = '0'
        cont_plant+=1
        m = f"<b>🌳🌲: </b> {cont_plant} \n"
        m += f"<b>🆔: </b> {data_data['_id']} \n"
        m += f"<b>⏱ cosecha: </b>  <code>{tiempo_cosecha}</code>  \n"
        m += f"<b>⏱☠ de Maceta: </b>  <code>{dead_matera}</code>  \n"
        m += f"<b>⏱☠💧: </b>  <code>{time_water}</code>  \n"
        m += f"<b>🦅: </b>  <code>{cuervo}</code>  \n"
        m += f"<b>¿Necesita agua? - </b>  <code>{data_data['needWater']}</code>  \n"
        a = data_data['plant']['iconUrl']           
        texto = texto+m+"\n"
    utc = f"<b>Hora UTC: </b>  <code>{datetime.utcnow().strftime('%H:%M:%S')}</code>  \n"
    print('Working general')
    """ print(str(texto+utc)) """
    return(texto+utc)