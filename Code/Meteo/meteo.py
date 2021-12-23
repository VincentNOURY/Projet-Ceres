"""Uses an API to get the meteorological forecast and prints it"""

import json
import math
import requests
from datetime import date as datetime
from datetime import timedelta

def get_meteo() -> dict:
    """
        Args: None

        Return: Dictionary that contains the amout of rain per day (date format : yyyy-mm-dd)

        Requests a public API for the meteorological forecast (over a week including yesterday).
        Prints out the detailled results and then prints out the day per day
        And returns the dictionary containing theeses values
    """

    url = "http://www.infoclimat.fr/public-api/gfs/json\
    ?_ll=48.85341,2.3488&_auth=AhhTRFMtBCYDLgA3D3lReFI6BjMPeQMkVysKaVo%2FUy4DaA\
    BhAWFTNQdpUC0HKAo8V3pXNAE6AzNTOAN7CHpXNgJoUz9TOARjA2wAZQ8gUXpSfAZnDy8DJFc8C\
    m9aKVM2A2UAegFjUzIHbVAsBzYKNldlVygBIQM6UzYDZwhhVzMCYFMzUzgEbwNkAH0PIFFjUmAG\
    YA9mA2hXMQpsWjVTZQNmADcBYFM0B2BQLAc2CjxXYlcxATwDPlM2A2wIelcrAhhTRFMtBCYDLgA\
    3D3lReFI0BjgPZA%3D%3D&_c=bc0b6c355d4a1f89b826625db56f406f"

    res = requests.get(url = url, allow_redirects = True)
    data = json.loads(res.text) #Dictionary containg the result of the API call

    if data["request_state"] == "200" or data["message"] == "OK":
        #for key in list(data.keys())[5:]:
            #print(f"date : {key}  ==> pluie : {data[key]['pluie']}")

        #print("Total de pluie pour la journée (en mm) :")
        date = list(data.keys())[5].split(" ")[0]
        tot = float(data[list(data.keys())[5]]["pluie"])
        rain = {}

        for key in list(data.keys())[6:]:
            if date != key.split(" ")[0]:
                rain[key.split(" ")[0]] = math.ceil(tot)
                #print(f"{date} : {math.ceil(tot)} mm")
                date = key.split(" ")[0]
                tot = 0
            tot += float(data[key]['pluie'])

        rain[key] = math.ceil(tot)
        #print(f"{date} : {math.ceil(tot)} mm")

    return rain

def diff_dates(date1 : str, date2 = str(datetime.today())):
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


def write_to_json(path : str):
    url = "http://www.infoclimat.fr/public-api/gfs/json\
    ?_ll=48.85341,2.3488&_auth=AhhTRFMtBCYDLgA3D3lReFI6BjMPeQMkVysKaVo%2FUy4DaA\
    BhAWFTNQdpUC0HKAo8V3pXNAE6AzNTOAN7CHpXNgJoUz9TOARjA2wAZQ8gUXpSfAZnDy8DJFc8C\
    m9aKVM2A2UAegFjUzIHbVAsBzYKNldlVygBIQM6UzYDZwhhVzMCYFMzUzgEbwNkAH0PIFFjUmAG\
    YA9mA2hXMQpsWjVTZQNmADcBYFM0B2BQLAc2CjxXYlcxATwDPlM2A2wIelcrAhhTRFMtBCYDLgA\
    3D3lReFI0BjgPZA%3D%3D&_c=bc0b6c355d4a1f89b826625db56f406f"

    res = requests.get(url = url, allow_redirects = True)
    data = json.loads(res.text)
    final = {"0": {}, "1":{}, "2":{}}
    final_temp = {"0": {}, "1":{}, "2":{}}

    if data["request_state"] == "200" or data["message"] == "OK":
        keys = list(data.keys())[6:]
        for key in keys:
            date, hour = key.split(" ")
            diff = -diff_dates(date)
            if diff >= 0 and diff <= 2:
                final[str(diff)][hour.split(":")[0]] = data[date + " " + hour]["pluie"]
                final_temp[str(diff)][hour.split(":")[0]] = int(data[date + " " + hour]["temperature"]["sol"] - 273)

    with open(path + "/pluie.json", 'r') as file:
        temp = json.loads(file.read())
        for key in list(temp.keys())[:6]:
            if key not in data.keys():
                final[key] = temp[key]

    with open(path + "/temperature.json", 'r') as file:
        temp = json.loads(file.read())
        for key in list(temp.keys())[:6]:
            if key not in data.keys():
                final_temp[key] = temp[key]

    with open(path + "/pluie.json", 'w') as file:
        json.dump(final, file)

    with open(path + "/temperature.json", 'w') as file:
        json.dump(final_temp, file)
    return final, final_temp

def main():

    """
    Description : main function is called only if the file is called directly
    """

    get_meteo()
    #meteo = get_meteo()
    #print(dict)

if __name__ == '__main__':
    main()
