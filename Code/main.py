from WebServer.web_server import start as start_server
#from Capteur.Tout_en_un import arroser
from Meteo.meteo import write_to_json
from Meteo.meteo import diff_dates
from Meteo.meteo import get_meteo
from datetime import timedelta
from datetime import date
from time import sleep
from logs import log
import threading
import json


SEUIL = 3
ATROPLU = 10
TROUMID = 30
DELAY = 3600 # time between checks
TEMPS_ARROSAGE = 30

def calcul_arrosage(dernier_arrosage : str):
    """
    Description : Calcule l'estimation du prochain arrosage

    Args :
        - dernier_arrosage : date (format : yyyy-mm-dd)

    Return :
    """
    log("debug", "Start of calcul_arrosage")
    with open("WebServer/templates/pluie.json", 'r') as file:
        s=0
        pluie = json.loads(file.read())
        for i in pluie.keys():
            for j in pluie[i].keys():
                s = s + int(pluie[i][j])
    h=0
    a=0
    with open("WebServer/Capteurs info/Capteurs.json") as file:
        humidite = json.loads(file.read())
        for i in humidite.keys():
            h = h + int(humidite[i]["humidity"])
        a = h/len(humidite.keys())

    if diff_dates(dernier_arrosage)>=SEUIL:
        if s < ATROPLU and a < TROUMID:
            log("debug", "Arrosage")
            dernier_arrosage = str(date.today())
            #arroser(90, TEMPS_ARROSAGE)

def creer_date(nb_days):
    return(str(date.today() + timedelta(days=1)))

def prevision_arrosage(dernier_arrosage):
    return creer_date(SEUIL - diff_dates(dernier_arrosage))

if __name__ == '__main__':
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    while True:
        dernier_arrosage = "2021-11-28"
        estimation_arrosage = prevision_arrosage(dernier_arrosage)
        pluie, temp = write_to_json("WebServer/templates")
        calcul_arrosage(dernier_arrosage)
        sleep(DELAY)
