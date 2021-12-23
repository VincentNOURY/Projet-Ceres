from Meteo.meteo import get_meteo
from Meteo.meteo import write_to_json
from Meteo.meteo import diff_dates
from datetime import date
from datetime import timedelta
from WebServer.web_server import start


SEUIL = 3

def calcul_arrosage(dernier_arrosage : str):
    """
    Description : Calcule l'estimation du prochain arrosage

    Args :
        - dernier_arrosage : date (format : yyyy-mm-dd)

    Return :
    """
    if diff_dates(dernier_arrosage) >= SEUIL:
        pass #arroser


def creer_date(nb_days):
    return(str(date.today() + timedelta(days=1)))

def prevision_arrosage(dernier_arrosage):
    return creer_date(SEUIL - diff_dates(dernier_arrosage))

if __name__ == '__main__':
    dernier_arrosage = "2021-11-28"
    estimation_arrosage = prevision_arrosage(dernier_arrosage)
    print(write_to_json("WebServer/templates"))
    #start()
