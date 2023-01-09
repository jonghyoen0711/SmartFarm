import Adafruit_DHT
import time
sensor = Adafruit_DHT.DHT11
pin=18

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
if humidity is not None and temperature is not None:
    while(1):
        print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
        time.sleep(2)
 
else:
    print('fail')