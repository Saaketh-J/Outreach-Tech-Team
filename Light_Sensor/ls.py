import rp2
from machine import Pin
from machine import ADC
from time import sleep
import utime
import time
import sys
 
# NOTES - I was able to adjust the light intensity via the blue box in the sensor
 
#establishing/displaying sytem information
print("System info: ")
print (str(sys.implementation))
print()
print()

#displaying and setting the time
print("System time: ")
rtc = machine.RTC()
timestamp = rtc.datetime()
timestring="%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3] + timestamp[4:7])
print("Date and time: " + timestring)
print()
print()


#creating and opening file to store sensor data
file = open ("sensordata.txt", "w")
 
## This first section can check if the Light is Above or Below a certain threshold
## The light sensor value can be tweaked to print/output a specific message based on
## The amount of light. 1 Represents a high analog signal, and 0 a low signal
 
# light_sensor = Pin(0,Pin.IN)
# 
# while True:
#     if light_sensor.value() == 1:
#         print("No light detected")
#         sleep(2)
#     else:
#         print("light detected")
#         sleep(2)


# Takes the Light sensor Reading and Converts it
# to read and print the measured value from the LDR.
# The ‘u16’ part translates the binary value in an unsigned 16-bit integer

# ldr = machine.ADC(27)
#  
# while True:
#     light = ldr.read_u16()
#     print(f"light sensor reading: {light}")
# #    print(ldr.read_uv())
#     time.sleep(2)
    

# take the light sensor and via an analog reading and some math,
# convert it to a percentage- a more readble understanding
# and probably the most useful case when coordinated with a timestamp
# and sent into a file

photoPIN = 27
def readLight(photoGP):
    photoRes = ADC(Pin(photoPIN))
    light = photoRes.read_u16()
    light = round(light/65535*100,2)
    return light
    
#continuous run loop

while True:
    file = open ("sensordata.txt", "w")
    file.read()
    file.write(timestring + ", temp: " + str(readLight(photoPIN)) +"%")
    file.close()
    print("light: " + str(readLight(photoPIN)) +"%")
    sleep(2) # set a delay between readings

    
# SAMPLE OUTPUT
#light: 17.31%
#light: 19.29%
#light: 5.39%
#light: 5.19%
