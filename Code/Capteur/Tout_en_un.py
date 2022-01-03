import RPi.GPIO as GPIO
import board as board
import requests as requests
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)

pwm = GPIO.PWM(3, 50)
pwm.start(0)


def arrosage(angle, temps):
    mvm = angle / 18 + 2
    GPIO.output(3, True)
    pwm.ChangeDutyCycle(mvm)
    time.sleep(1)
    GPIO.output(3, False)
    pwm.ChangeDutyCycle(0)
    time.sleep(temps)


dhtDevice = adafruit_dht.DHT22(board.D18)

if __name__ == "__main__":
    while True:
        try:
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidite = dhtDevice.humidity
            log('debug', "Temperature: {:.1f} F / {:.1f} C    Humidite: {}% ".format(temperature_f, temperature_c, humidite))
            requests.post(url="http://127.0.0.1:5000/capteurs", data={"id": id, "humidity": humidite, "temp": temperature_c})

        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

        time.sleep(2.0)
