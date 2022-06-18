import random
import telebot
from telebot import types
import json
import os
from dotenv import load_dotenv, find_dotenv
from pprint import pprint
from json import JSONEncoder, loads
import scrapping
import scrapping_tree
import schedule
import app
from threading import Thread
from time import sleep

class ToJson(JSONEncoder):
        def default(self, o):
            return o.__dict__ 
load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

flag_data_json = False
data = {}
token= ''
data['config'] = []

try:
    with open('data.json') as file:
        data = json.load(file)
except:
  print("No hay data")
  flag_data_json=True
pprint(data)


def uno():
    count = 0
    for data_ in data["config"]:
        if app.get_user_active(data_["id"]) == True:
            bot.send_message(data_["id"], scrapping.messsage_info_general(data_["token"]), parse_mode=os.getenv('PARSE_MODE'))    
            bot.send_message(data_["id"], str(data_["username"]))
        count = 1

def dos():
    for data_ in data["config"]:
        if app.get_user_active(data_["id"]) == True:
            alerta = scrapping.messsage_info(data_["token"])        
            if not alerta:
                print("Empty")
            else:            
                for i in alerta:
                    print(i)
                    bot.send_message(data_["id"], i, parse_mode=os.getenv('PARSE_MODE'))
def tres():
    for data_ in data["config"]:
        if app.get_user_active(data_["id"]) == True:
            alerta = scrapping_tree.messsage_info_tree(data_["token"])
            if not alerta:
                print("Empty")
            else:
                print(alerta)
                for i in alerta:
                    bot.send_message(data_["id"], i, parse_mode=os.getenv('PARSE_MODE'))
def cuatro():
    for data_ in data["config"]:      
        if app.get_user_active(data_["id"]) == True:          
            bot.send_message(data_["id"], scrapping_tree.messsage_info_tree_general(data_["token"]), parse_mode=os.getenv('PARSE_MODE'))

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)
        
# Create the job in schedule.
uno()
dos()
tres()
cuatro()
schedule.every(random.randint(60, 70)).minutes.do(uno)
schedule.every(random.randint(10, 30)).minutes.do(dos)
schedule.every(random.randint(60, 70)).minutes.do(tres)
schedule.every(random.randint(120, 140)).minutes.do(cuatro)

# Spin up a thread to run the schedule check so it doesn't block your bot.
# This will take the function schedule_checker which will check every second
# to see if the scheduled job needs to be ran.
Thread(target=schedule_checker).start()

def getUpdates():
    a = ToJson().encode(bot.get_updates())
    a = json.loads(a)
    return a

info = {
    'TOKEN' : 'Para obtener el TOKEN DE SESION Bearer de Plants Vs Undead deber de ejecutar el siguiente codigo en la consola de Herramienta para desarrolladores',
    'codigo' : 'var x = localStorage.getItem("token"); x',    
    }
         
commands = {
    "/help" : "Muestra todos los comandos en los que puedes interactuar",
    "/messsage_info_tree" : "Muestra la informacion relevante del arbol del mundo Se ejecuta cada Hora",
    "/messsage_info_tree_general" : "Muestra la información general del arbol",
    "/messsage_info" : "Muestra la Las alertas de tu granja",
    "/messsage_info_general" : "Muestra la informacion general de tu granja",
    "/info" : "Información de registro ",
    }

def request_create_user(database):
    flag_= False
    for data_ in data["config"]:   
        if data_["id"] == database[0]  and data_["token"] == database[2]:
            flag_= True
            bot.send_message(database[0], 'Ya te encuentras registrado', parse_mode='HTML')
    if flag_ == False: #Entra a registrarse
        bot.send_message(database[0], 'Estamos validando los datos', parse_mode='HTML')                        
        data['config'].append({
            'id':database[0],
            'username':database[1],
            'token':database[2],
        })
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
        texto =''
        m = f"<b>Usuario: </b> <code> {database[1]} </code> \n"
        m += f"<b> acaba de ser registrado con el id: </b> <code>{database[0]}</code> \n"        
        m += f"<code>Ya puedes ver tu información de Plants Vs Undead </code>  \n"
        m += f"<code>Mira que puede hacer con el comando</code>  \n"
        m += "/help"
        texto = texto+m+"\n"
        bot.send_message(database[0], texto, parse_mode='HTML')
    print('Creancion de usuario')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,f"<b> Espera un momento...</b>",parse_mode=os.getenv('PARSE_MODE'))
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    username = str(json_["from_user"]["username"])    
    if app.get_user(private_id) == False:            
        bot.send_message(private_id,f"Usuario: <code>{str(username)}</code> NO se encuentra registrado",parse_mode=os.getenv('PARSE_MODE'))
    else:
        if flag_data_json:
            if app.get_user_active(private_id):
                data_ = app.get_all_data_user_active(private_id)
                request_create_user(data_)
        else:                            
            bot.send_message(private_id,f"Usuario: <code>{str(username)}</code> ya se encuentra registrado",parse_mode=os.getenv('PARSE_MODE'))            


##########################################Comandos##########################################

@bot.message_handler(commands=['messsage_info_tree'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    for data_ in data["config"]:   
        if data_["id"] == str(private_id):   
            if app.get_user_active(private_id) == True:         
                alerta = scrapping_tree.messsage_info_tree(data_["token"])
                if not alerta:
                    print("Empty")
                else:
                    print(alerta)
                    for i in alerta:
                        bot.send_message(private_id, i, parse_mode=os.getenv('PARSE_MODE'))
            else:
                bot.send_message(private_id, 'Usuario inactivo', parse_mode=os.getenv('PARSE_MODE'))

        else:
            bot.send_message(private_id, 'No has iniciado el bot', parse_mode=os.getenv('PARSE_MODE'))

@bot.message_handler(commands=['messsage_info_tree_general'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    for data_ in data["config"]:   
        if data_["id"] == str(private_id):
            if app.get_user_active(private_id) == True:
                bot.send_message(private_id, scrapping_tree.messsage_info_tree_general(data_["token"]), parse_mode=os.getenv('PARSE_MODE'))
            else:
                bot.send_message(private_id, 'Usuario inactivo', parse_mode=os.getenv('PARSE_MODE'))
        else:
            bot.send_message(private_id, 'No has iniciado el bot', parse_mode=os.getenv('PARSE_MODE'))
            
@bot.message_handler(commands=['messsage_info_general'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    for data_ in data["config"]:   
        if data_["id"] == str(private_id):
            if app.get_user_active(private_id) == True:
                bot.send_message(private_id, scrapping.messsage_info_general(data_["token"]), parse_mode=os.getenv('PARSE_MODE'))
            else:
                bot.send_message(private_id, 'Usuario inactivo', parse_mode=os.getenv('PARSE_MODE'))
        else:
            bot.send_message(private_id, 'No has iniciado el bot', parse_mode=os.getenv('PARSE_MODE'))

@bot.message_handler(commands=['messsage_info'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    for data_ in data["config"]:
        print(data_["id"])
        print(private_id)
        if data_["id"] == str(private_id):
            if app.get_user_active(private_id) == True:
                alerta = scrapping.messsage_info(data_["token"])            
                print(alerta)
                if not alerta:
                    print("GOOD")
                    bot.send_animation(private_id,'https://c.tenor.com/bEBxkuyFiucAAAAC/yes-nice.gif', caption='No tienes ninguna alerta de tu granja\nStatus: <code>GOOD</code>', parse_mode=os.getenv('PARSE_MODE'))
                else:
                    print(alerta)
                    for i in alerta:
                        bot.send_message(private_id, i, parse_mode=os.getenv('PARSE_MODE'))
            else:
                bot.send_message(private_id, 'Usuario inactivo', parse_mode=os.getenv('PARSE_MODE'))
        else:
            bot.send_message(private_id, 'No has iniciado el bot', parse_mode=os.getenv('PARSE_MODE'))




@bot.message_handler(commands=['info'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    for info_ in info: 
        bot.send_message(private_id, info[info_])

@bot.message_handler(commands=['Address'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    for info_ in info: 
        bot.send_message(private_id, info[info_])
@bot.message_handler(commands=['help'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    bot.send_message(private_id, '<a href="t.me/utilitiesPVU_bot">utilities Plant Vs Undead</a>',parse_mode=os.getenv('PARSE_MODE'))
    texto=''
    markup = types.ReplyKeyboardMarkup()        
    if app.get_user_active(private_id) == True:     
        for command_ in commands:
            texto += command_+': '+commands[command_]+'\n'
            markup.row(command_)
        bot.send_message(private_id, texto,reply_markup=markup,parse_mode=os.getenv('PARSE_MODE'))
    else:
        bot.send_message(private_id, 'No te encuentras registrado',reply_markup=markup,parse_mode=os.getenv('PARSE_MODE'))        
    bot.send_message(private_id, 'Debes inciar el bot para visualizar tu información /start para inciarlo',reply_markup=markup,parse_mode=os.getenv('PARSE_MODE'))

bot.infinity_polling()