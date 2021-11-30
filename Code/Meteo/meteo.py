"""Uses an API to get the meteorological forecast and prints it"""

import json
import math
import requests

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

def main():

    """
    Description : main function is called only if the file is called directly
    """

    get_meteo()
    #meteo = get_meteo()
    #print(dict)

if __name__ == '__main__':
    main()
