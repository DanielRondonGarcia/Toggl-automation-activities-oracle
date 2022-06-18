import json
from logging import captureWarnings
from bs4 import BeautifulSoup
import requests
from requests.structures import CaseInsensitiveDict
import gspread
from json import JSONEncoder
from datetime import datetime,timedelta
from google.oauth2.service_account import Credentials
import os
import re
import telebot
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

class ToJson(JSONEncoder):
        def default(self, o):
            return o.__dict__ 

def parse_timedelta(stamp):
    if 'day' in stamp:
        m = re.match(r'(?P<d>[-\d]+) day[s]*, (?P<h>\d+):'
                     r'(?P<m>\d+):(?P<s>\d[\.\d+]*)', stamp)
    else:
        m = re.match(r'(?P<h>\d+):(?P<m>\d+):'
                     r'(?P<s>\d[\.\d+]*)', stamp)
    if not m:
        return ''

    time_dict = {key: float(val) for key, val in m.groupdict().items()}
    if 'd' in time_dict:
        return timedelta(days=time_dict['d'], hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])
    else:
        return timedelta(hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])

def get_user(id_user):
    print('check user data')
    scopes = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file(
        os.getenv('CREDENTIALS_JSON'),        
        scopes=scopes
    )
    client = gspread.authorize(creds)
    sh = client.open("data_pvu")
    shw = sh.get_worksheet(3)
    id_ = shw.find(str(id_user))          
    if id_:
        values_list = shw.row_values(id_.row)
        if values_list[3] == 'INACTIVO':
            print('Existing user INACTIVO')
            bot.send_message(values_list[0], text='Tu suscripcion se encuentra INACTIVA\n Deber volver a pagar la suscripcion para activarla\n Visita el bot de configuración <a href="t.me/utilitiesPVU_bot">utilities Plant Vs Undead</a>',parse_mode=os.getenv('PARSE_MODE'))
            return True
        elif values_list[3] == 'PENDIENTE':
            print('Existing user PENDIENTE')
            bot.send_message(values_list[0], text='Tu suscripcion se encuentra PENDIENTE de activación',parse_mode=os.getenv('PARSE_MODE'))
            return True
        elif values_list[3] == 'ACTIVO':
            print('Existing user ACTIVO')
            try:
                time_ = datetime.strptime(values_list[4].replace("'",''), '%Y-%m-%d %H:%M:%S')
            except:
                time_ = datetime.strptime(values_list[4].replace("'",''), '%Y-%m-%dT%H:%M:%S')
            today = datetime.utcnow()            
            diferencia = today-time_        
            bot.send_message(values_list[0], text='Tu suscripcion se encuentra ACTIVA y EXPIRA en: '+str(parse_timedelta(values_list[5]) - diferencia),parse_mode=os.getenv('PARSE_MODE'))
            return True    
    return False

def get_user_active(id):
    print('check user data')
    scopes = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file(
        os.getenv('CREDENTIALS_JSON'),        
        scopes=scopes
    )
    client = gspread.authorize(creds)
    sh = client.open("data_pvu")
    shw = sh.get_worksheet(3)
    id_ = shw.find(str(str(id)))          
    if id_:
        values_list = shw.row_values(id_.row)
        if values_list[3] == 'ACTIVO':
            print('Existing user')
            return True
        else:
            print('Usuario se encuentra: '+values_list[3]+' '+values_list[1])
            bot.send_message(values_list[0], text='Tu cuenta aun se encuentra: '+ str(values_list[3]) ,parse_mode=os.getenv('PARSE_MODE'))
            return False
    print('User not registered ')
    return False

def get_all_data_user_active(id):
    print('check user data')
    scopes = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file(
        os.getenv('CREDENTIALS_JSON'),        
        scopes=scopes
    )
    client = gspread.authorize(creds)
    sh = client.open("data_pvu")
    shw = sh.get_worksheet(3)
    id_ = shw.find(str(str(id)))          
    if id_:
        values_list = shw.row_values(id_.row)
        if values_list[3] == 'ACTIVO':
            print('Existing user')
            values_list = shw.row_values(id_.row)
            return values_list
        else:
            print('Usuario se encuentra: '+values_list[3]+' '+values_list[1])
            bot.send_message(values_list[0], text='Tu cuenta aun se encuentra: '+ str(values_list[3]) ,parse_mode=os.getenv('PARSE_MODE'))        
