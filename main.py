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
                  port=8883, keepalive=10, ssl=True)

led = Pin(2, Pin.OUT)
i2c = I2C(scl=Pin(21), sda=Pin(22), freq=400000)  
d = AHT10(i2c,0,0x38)

HIGH_THRESHOLD = 35
LOW_THRESHOLD = 30
ALARM_FLAG = False


contador = 0

def heartbeat(nada):
    global contador
    if contador > 5:
        pulsos.deinit()
        contador = 0
        return
    led.value(not led.value())
    contador += 1
  
def transmitir(pin):
    print("publicando")
    mqtt.connect()
    mqtt.publish(f"iot/{CLIENT_ID}",datos)
    mqtt.disconnect()
    pulsos.init(period=150, mode=Timer.PERIODIC, callback=heartbeat)

#publicar = Timer(0)
#publicar.init(period=30000, mode=Timer.PERIODIC, callback=transmitir)
pulsos = Timer(1)

while True:
    try:
        #d.measure()
        temperatura = d.temperature()
        humedad = d.humidity()
        datos = json.dumps(OrderedDict([
            ('temperatura',temperatura),
            ('humedad',humedad)
        ]))
        print(datos)
        if temperatura > HIGH_THRESHOLD and not ALARM_FLAG:  # Si la temperatura sube por encima de un límite superior y aún no se transmitió nada, transmite
            transmitir()
            ALARM_FLAG = True  # La bandera impide retransmitir los datos si la temperatura no baja por debajo del límite inferior

        if temperatura < LOW_THRESHOLD:
            ALARM_FLAG = False  # Cuando la temperatura decae por debajo el límite inferior, se desactiva la bandera

    except OSError as e:
        print("sin sensor")
    time.sleep(5)
