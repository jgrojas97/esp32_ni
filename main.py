# AHT10 I2C test ROJAS JUan
from machine import Pin
from machine import I2C
from aht10 import AHT10
import time

i2c = I2C(scl=Pin(22), sda=Pin(23), freq=400000)  
aht10 = AHT10(i2c,0,0x38)

print("Inicializado")

while True:
    aht10.print()
    time.sleep_ms(2000)
