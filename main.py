# Germán Andrés Xander 2023

from machine import Pin, Timer, unique_id, I2C
from aht10 import AHT10
import time
import json
import ubinascii
from collections import OrderedDict
from settings import SERVIDOR_MQTT
from umqtt.robust import MQTTClient

CLIENT_ID = ubinascii.hexlify(unique_id()).decode('utf-8')

mqtt = MQTTClient(CLIENT_ID, SERVIDOR_MQTT,
                  port=8883, keepalive=40, ssl=True)

sw = Pin(23, Pin.IN, Pin.PULL_DOWN)
led = Pin(2, Pin.OUT)
i2c = I2C(scl=Pin(21), sda=Pin(22), freq=400000)  
d = AHT10(i2c,0,0x38)


def sub_cb(topic, msg):
    print((topic, msg))
    if msg==b"apagar":      #Texto viene codificado como binario
        led.value(0)
    if msg==b"encender":
        led.value(1)

mqtt.set_callback(sub_cb)
mqtt.connect()
mqtt.subscribe(f"iot/{CLIENT_ID}/comando")

def transmitir(pin):
    mqtt.publish(f"iot/{CLIENT_ID}",datos)

timer1 = Timer(1)
timer1.init(period=20000, mode=Timer.PERIODIC, callback=transmitir)

datos={}

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
    mqtt.check_msg()
    time.sleep(5)

mqtt.disconnect()
