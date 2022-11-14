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

#creating counter for number of times it has detected activity
# count = int()

#continuous run loop that is the main program
led.value(0)
count = 0
while True:
    file = open ("sesnsordata.txt", "w")
    file.read()
    file.write(timestring + ", temp: " + str(temp) + ' C ' + "\n")
    file.close()
    #print("Times activity detected: " + str(count))
     
    if count >=50:
        print("Real interaction detected")
        file = open ("count.txt", "a")
        file.write("human detected with a temperature of " + str(temp) + " C° at " + str(timestring) + "\n" )
        file.close()
        count = 0
#    if count < 20 and count >18:
#        count = 0
     
    #no movement detected
    if PIR_Sensor.value()==0:
        led.value(0)
   #     print("No activity detected.")  
        #sleep(0.01)
   
    #detecting movement
    else:
        led.value(1)
    #    print("human detected and the temperature is " + str(temp) + "degrees celsius.")
        file = open ("sensorvalues.txt", "a")
        file.write("human detected and the ambient temp is " + str(temp) + " at " + str(timestring) + "\n")
        file.close()
        count +=1
        print(count)
        
        
        
            
        

        
        #count++
        
        
        
        #sleep(0.01)
        
#file.close()

#if you wish to write out data lingering in program to the actual file, use:
#file.flush()




