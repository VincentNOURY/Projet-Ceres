import Constellation
import RPi.GPIO as GPIO, time, os      
 
MAX_READING = 30000
LIGHT_SENSOR_GPIO = 18
MEASURE_INTERVAL = 10
 
def OnExit():
    GPIO.cleanup()
 
def RCtime (RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1) 
    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(RCpin) == GPIO.LOW):
        if (reading > MAX_READING):
            break
        reading += 1
    return reading
 
def Start():
    global INTERVAL
    GPIO.setmode(GPIO.BCM)
    Constellation.OnExitCallback = OnExit
    lastSend = 0
    currentValue = 0
    count = 0
    Constellation.WriteInfo("Le capteur est pret !")
    while Constellation.IsRunning:
        currentValue = currentValue + RCtime(LIGHT_SENSOR_GPIO)
        count = count + 1
        ts = int(round(time.time()))
        if ts - lastSend >= int(Constellation.GetSetting("Interval")):
            avg = int(round(currentValue / count))
            Constellation.PushStateObject("Luminosité", avg, "int")
            currentValue = 0
            count = 0
            lastSend = ts
        time.sleep(MEASURE_INTERVAL)
 
Constellation.Start(Start)