# This program is using the Raspberry Pi Pico to gather data using a simple tilt 
# This was written using MicroPython version 1.19.1

from machine import Pin
import utime as time
from dht import DHT11, InvalidChecksum

# Connect the Pico's GP1 to ht11 sensor's DAT pin.
# Connect the Pico's 3.3V Pin to ht11 sensor's VCC pin.
# Connect the Pico's GND pin to ht11 sensor's GND pin.
dhtPIN = 3
dhtSensor = DHT11(Pin(dhtPIN, Pin.OUT, Pin.PULL_DOWN))

# Print the temperature followed by the humidity
while True:
    print("Temp: {}°C".format(dhtSensor.temperature), "| Hum: {0:.1%}".format(dhtSensor.humidity/100))
    time.sleep(1.1)
