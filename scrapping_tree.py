from bs4 import BeautifulSoup
import time
import requests
from requests.structures import CaseInsensitiveDict
import json
from datetime import datetime,timedelta
def time_exchange():
    s1 = "00:00:00"
    ahora = datetime.utcnow().strptime('%H:%M:%S')
    dentro_de_1_hora = ahora + timedelta(hours=1)
    return("Dentro de una hora: " + str(dentro_de_1_hora))
    
def request_api(bearer):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer "+bearer
    url_result = requests.get('https://backend-farm.plantvsundead.com/world-tree/datas', headers=headers)
    soup = BeautifulSoup(url_result.content, 'html.parser')
    site_json=json.loads(soup.text)
    return site_json

def messsage_info_tree(bearer):
    data_print = []
    data = request_api(bearer)
    m0 = f"💧<b> Nivel Actual: </b> {data['data']['level']} \n"        
    m0 += f"<b>Total Agua: </b>  <code>{'{:,}'.format(data['data']['totalWater'])}</code>  \n"
    m0 += f"<b>Agua que aportaste: </b>  <code>{data['data']['myWater']}</code>  \n"
    if data['data']['yesterdayReward']:
        m0 += f"<b>Recompensa de ayer: </b>  <code>{data['data']['yesterdayReward']}</code>  \n"    
    data_print.append(m0)
    if data['data']['level'] == len(data['data']['reward']):
        alerta = f" ¡ATENCIÓN! 🌲🌳 Se completo el arbol del mundo: Tienes hasta las 7:00 PM\nApurate y ve a reclamarlos\nhhttps://marketplace.plantvsundead.com/login#/worldtree\n"
        data_print.append(alerta)                      
    print('Working tree')    
    return(data_print)

def messsage_info_tree_general(bearer):
    data = request_api(bearer)
    print(data)
    total = data["data"]["reward"][5]['target']
    total_ahora = data["data"]["totalWater"]
    m ="🌲🌳 Árbol del mundo 🌳🌲"+"\n\n"    
    m += f"🌱<b>Total: </b><code>"+str('{:,}'.format(total))+"</code>\n\n"
    for i in data["data"]["reward"]:
        tarjet = i["target"]
        if tarjet <= total_ahora:
            m += f"✅<b>:"+ str(i["type"]) +" </b><code><s>" + str('{:,}'.format(tarjet)) + "</s></code>\n"
        else:
            m += f"💦<b>:"+ str(i["type"]) +" </b><code>" + str('{:,}'.format(tarjet)) + " de " + str('{:,}'.format(total_ahora))+"</code>\n"

    m = m+"\n"
    print('Working tree General')
    return(m)
