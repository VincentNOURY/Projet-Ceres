from Meteo.meteo import get_meteo
from datetime import date
from datetime import timedelta


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


def diff_dates(date1 : str, date2 = str(date.today())):
    nb_days = { "01" : 31,
                "02" : 28,
                "03" : 31,
                "04" : 30,
                "05" : 31,
                "06" : 30,
                "07" : 31,
                "08" : 31,
                "09" : 30,
                "10" : 31,
                "11" : 30,
                "12" : 31,
                }

    date1 = date1.split("-")
    date2 = date2.split("-")
    years = int(date2[0]) - int(date1[0])
    months = int(date2[1]) - int(date1[1])
    days = int(date2[2]) - int(date1[2])
    months = months + years * 12
    days = days + months * nb_days[date2[1]]
    return days

def creer_date(nb_days):
    return(str(date.today() + timedelta(days=1)))

def prevision_arrosage(dernier_arrosage):
    return creer_date(SEUIL - diff_dates(dernier_arrosage))

if __name__ == '__main__':
    dernier_arrosage = "2021-11-28"
    estimation_arrosage = prevision_arrosage(dernier_arrosage)
