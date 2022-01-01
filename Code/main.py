from Meteo.meteo import get_meteo
from Meteo.meteo import write_to_json
from Meteo.meteo import diff_dates
from datetime import date
from datetime import timedelta
from WebServer.web_server import start


SEUIL = 3
ATROPLU = 10
TROUMID = 30

def calcul_arrosage(dernier_arrosage : str):
    """
    Description : Calcule l'estimation du prochain arrosage

    Args :
        - dernier_arrosage : date (format : yyyy-mm-dd)

    Return :
    """
    with open("WebServer/templates/pluie.json", 'r') as file:
        s=0
        pluie = json.loads(file.read())
        for i in pluie.keys():
            for j in i.keys():
                s = s + int(pluie[i][j])
        if diff_dates(dernier_arrosage)>=SEUIL:
            if s<ATROPLU:
                pass #arroser
    h=0
    a=0
    with open("WebServer/Capteurs info/Capteurs.json") as file:
        humidite = json.loads(file.read())
        for i in humidite.keys():
            for j in i.keys():
                h = h + int(humidite[i]["humidite"])
        a = h/len(humidite.keys())
        if a<TROUMID:
            pass #arroser

def creer_date(nb_days):
    return(str(date.today() + timedelta(days=1)))

def prevision_arrosage(dernier_arrosage):
    return creer_date(SEUIL - diff_dates(dernier_arrosage))

if __name__ == '__main__':
    dernier_arrosage = "2021-11-28"
    estimation_arrosage = prevision_arrosage(dernier_arrosage)
    pluie, temp = write_to_json("WebServer/templates")
    start()
