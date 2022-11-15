import machine
from machine import Pin, ADC
import utime
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


#led = Pin(0, Pin.OUT)
led = machine.Pin("LED", machine.Pin.OUT)
# please use 5 volts
# GP27 -> ADC1
photo_sensor = ADC(1)

count = 0
while (count < 51):
    print(photo_sensor.read_u16())
    sleep(2) # set a delay between readings
    count += 1

#my testing showed a range of values when exposed to light of 3088 - 3312 and when no light 65535