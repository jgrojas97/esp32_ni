# AHT10 I2C test ROJAS JUan
from machine import Pin
from machine import I2C
from aht10 import AHT10
import time

i2c = I2C(scl=Pin(22), sda=Pin(23), freq=400000)  
aht10 = AHT10(i2c,0,0x38)

print("Inicializado")

while True:
    temperatura = aht10.temperature()
    humedad = aht10.humidity()
    print(f"La temperatura actual es de {temperatura} *C")
    print(f"La humedad actual es de {humedad} %")
    time.sleep_ms(2000)
