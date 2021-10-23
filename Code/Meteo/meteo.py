import json
import requests
import math

def get_meteo() -> dict:
    """
        Args: None

        Return: Dictionary that contains the amout of rain per day (date format : yyyy-mm-dd)
        
        Requests a public API for the meteorological forecast (over a week including yesterday).
        Prints out the detailled results and then prints out the day per day
        And returns the dictionary containing theeses values
    """

    url = "http://www.infoclimat.fr/public-api/gfs/json?_ll=48.85341,2.3488&_auth=AhhTRFMtBCYDLgA3D3lReFI6BjMPeQMkVysKaVo%2FUy4DaABhAWFTNQdpUC0HKAo8V3pXNAE6AzNTOAN7CHpXNgJoUz9TOARjA2wAZQ8gUXpSfAZnDy8DJFc8Cm9aKVM2A2UAegFjUzIHbVAsBzYKNldlVygBIQM6UzYDZwhhVzMCYFMzUzgEbwNkAH0PIFFjUmAGYA9mA2hXMQpsWjVTZQNmADcBYFM0B2BQLAc2CjxXYlcxATwDPlM2A2wIelcrAhhTRFMtBCYDLgA3D3lReFI0BjgPZA%3D%3D&_c=bc0b6c355d4a1f89b826625db56f406f"
    res = requests.get(url = url, allow_redirects = True)
    data = json.loads(res.text) #Dictionary containg the result of the API call

    if data["request_state"] == "200" or data["message"] == "OK":
        for key in list(data.keys())[5:]:
            print(f"date : {key}  ==> pluie : {data[key]['pluie']}")

        print("Total de pluie pour la journée (en mm) :")
        date = list(data.keys())[5].split(" ")[0]
        tot = float(data[list(data.keys())[5]]["pluie"])
        dict = {}

        for key in list(data.keys())[6:]:
            if date != key.split(" ")[0]:
                dict[key.split(" ")[0]] = math.ceil(tot)
                print(f"{date} : {math.ceil(tot)} mm")
                date = key.split(" ")[0]
                tot = 0
            tot += float(data[key]['pluie'])

        dict[key] = math.ceil(tot)
        print(f"{date} : {math.ceil(tot)} mm")

    return dict

def main():
    dict = get_meteo()
    print(dict)
    LIMITE_ARROSAGE = 10 # en mm

if __name__ == '__main__':
    main()
