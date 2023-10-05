# Germán Andrés Xander 2023

from machine import Pin, Timer, I2C
from aht10 import  AHT10
import time
import json
from collections import OrderedDict
import urequests
from settings import TOKEN, CHATID

sw = Pin(23, Pin.IN)
led = Pin(2, Pin.OUT)

i2c = I2C(scl=Pin(21), sda=Pin(22), freq=400000)  
d = AHT10(i2c,0,0x38)

print("esperand pulsador")
contador=0
estado=False

def alternar(pin):
    global contador, estado
    if sw.value():
        if not estado:
            contador+=1
            print(contador)
            led.value(not led.value())
            try:
                data = {'chat_id': CHATID, 'text': datos}
                response = urequests.post("https://api.telegram.org/bot" + TOKEN + '/sendMessage', json=data)
                # print(response.text)
                response.close()
                print("envio correcto a telegram")
            except:
                print("fallo en el envio a telegram")
            estado = True
        else:
            estado = False

timer1 = Timer(1)
timer1.init(period=50, mode=Timer.PERIODIC, callback=alternar)

while True:
    try:
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