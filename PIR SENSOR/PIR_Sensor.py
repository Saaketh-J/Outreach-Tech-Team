#import statements
import rp2
from machine import Pin
from time import sleep
import utime
import time
import sys

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

#assigning pin values and setting up sensor
led = Pin(0,Pin.OUT)
PIR_Sensor = Pin(1, Pin.IN)

#setting up temp to record
sensorTemp = machine.ADC(machine.ADC.CORE_TEMP)
conversionFactor = 3.3/ (65535)
read = sensorTemp.read_u16() * conversionFactor
temp = 27 - (read - 0.706)/0.001721



#continuous run loop
led.value(0)
while True:
    file = open ("sesnsordata.txt", "w")
    file.read()
    file.write(timestring + ", temp: " + str(temp) + ' C ' + "\n")
    file.close()
    
    if PIR_Sensor.value()==0:
        led.value(0)
        print("human not detected and the ambient temp is " + str(temp) + " degrees Celsius.")
        file = open ("sensorvalues.txt", "w")
        file.write("human not detected and the ambient temp is " + str(temp))
        file.close()
        
        #sleep(0.01)
    else:
        led.value(1)
        print("human detected and the temperature is " + str(temp) + " degrees celsius.")
        file = open ("sensorvalues.txt", "w")
        file.write("human detected and the ambient temp is " + str(temp))
        file.close()
        
        #sleep(0.01)
        
#file.close()

#if you wish to write out data lingering in program to the actual file, use:
#file.flush()


