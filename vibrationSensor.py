from machine import Pin
import time
from time import sleep
import sys

# Print the Raspberry Pi Pico system information:
#   Welcome, here is the system info:
#   (name='micropython', version=(1, 19, 1), _machine='Raspberry Pi Pico with RP2040', _mpy=4358)

print('Welcome, here is the system info:')
print (str(sys.implementation))
print()

# Timestamp class RTC will set time correctly when using Thonny and connected to a computer and manually initiated
# otherwise clock will init to the wrong value of 2021-01-01 00:00:01
rtc=machine.RTC()
timestamp=rtc.datetime()
timestring="%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3] + timestamp[4:7])

print ('Date and Time = ' + timestring)

vibration_pin = Pin(1, Pin.IN, Pin.PULL_UP)
red_led = Pin(0, Pin.OUT)
blue_led = Pin(2, Pin.OUT)

# can detect a waterbottle being dropped

try:
    while (True):
        #print(vibration_pin.value())
        if vibration_pin.value() == 1:
            red_led.value(1)
            blue_led.value(0)
            print("Vibrating")
            sleep(0.5)
            red_led.value(0)
            
        elif vibration_pin.value() == 0:
            #print(vibration_pin.value())
            #print("not vibrating")
            red_led.value(0)
            blue_led.value(1)
            sleep(0.5)
            
except KeyboardInterrupt:
    print("BYE")