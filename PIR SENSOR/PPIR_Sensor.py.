from machine import Pin
from time import sleep
import sys

led = Pin(0,Pin.OUT)
PIR_Sensor = Pin(1, Pin.IN)

while True:
    if PIR_Sensor.value()==0:
        print("human not detected")
        led.value(0)
        sleep(0.05)
    else:
        print("human detected")
        led.value(1)
        sleep(0.05)

