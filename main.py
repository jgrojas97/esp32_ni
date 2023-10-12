# Germán Andrés Xander 2023

from machine import Pin, I2C
from aht10 import AHT10
import time
import json
from collections import OrderedDict
import urequests
from settings import TOKEN, CHATID
from debounce import DebouncedSwitch

sw = Pin(23, Pin.IN, Pin.PULL_DOWN)
led = Pin(2, Pin.OUT)

i2c = I2C(scl=Pin(21), sda=Pin(22), freq=400000)  
d = AHT10(i2c,0,0x38)


print("esperand pulsador")
contador=0

def alternar(nada):
    global contador
    contador+=1
    print(contador)
    led.value(not led.value())
    try:
        data = {'chat_id': CHATID, 'text': datos}
        response = urequests.post("https://api.telegram.org/bot" + TOKEN + '/sendMessage', json=data)
        response.close()
        print("envio correcto a telegram")
    except:
        print("fallo en el envio a telegram")


objeto=DebouncedSwitch(sw, alternar)

while True:
    try:
        #d.measure()
        temperatura=d.temperature()
        humedad=d.humidity()
        datos=json.dumps(OrderedDict([
            ('temperatura',temperatura),
            ('humedad',humedad)
        ]))
        print(datos)
    except OSError as e:
        print("sin sensor")
    time.sleep(5)
