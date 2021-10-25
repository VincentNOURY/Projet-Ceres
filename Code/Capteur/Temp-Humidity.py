import time
import board
import adafruit_dht
import requests

dhtDevice = adafruit_dht.DHT22(board.D18)


while True :
    try :
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidite = dhtDevice.humidity
        print("Température: {:.1f} F / {:.1f} C    Humidité: {}% ".format(temperature_f, temperature_c, humidite))
        requests.post(url = "", data = {"id" : id, "humidity" : humidite, "temp" = temperature_c})

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)