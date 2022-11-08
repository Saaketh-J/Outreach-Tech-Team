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


led = Pin(0, Pin.OUT)
# GP26 -> ADC0
sound_sensor = ADC(0)

def sound_map(read_value, in_min, in_max, out_min, out_max):
    return (read_value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

count = 0
while (True):
    #print(sound_sensor.read_u16()) # prints the adc values
    # print(sound_sensor.read_u16() * 3.3 / 65536) # prints the voltage
    sound_level = round(sound_map(sound_sensor.read_u16(), 0, 65535, 0, 1000))
    if sound_level:
        # print("Sound Level: ", sound_level)
        # baseline is around 800~900 ish for some reason
        # baseline voltage is around 2.7 (@ 800 sound_level) and 3.2 (# 900 sound level)
        # when there is a sudden sound, voltage drops, and so the sound_level drops to around 35
        # a lightly louder than normal speaking voice and dropping a waterbottle onto wood right next
        # to the sensor both trigger this, and both result in the same voltage and sound_level
        # so basically this can detect a sudden loudness in a quiet room
        if sound_level < 40:
            print(sound_sensor.read_u16() * 3.3 / 65536) # prints the voltage
            print("Detect Noise! Sound level is: ", sound_level)
            print("Count: ", count, "\n")
            led.value(1)
            count += 1
        else:
            led.value(0)
        sleep(0.5)
