import machine
from machine import Pin, ADC
import rp2
import utime
import time
from time import sleep
import sys
from collections import deque
from dht import DHT11, InvalidChecksum


# Print the Raspberry Pi Pico system information:
#   Welcome, here is the system info:
#   (name='micropython', version=(1, 19, 1), _machine='Raspberry Pi Pico with RP2040', _mpy=4358)

print('Welcome, here is the system info:')
print(str(sys.implementation))
print()

# Timestamp class RTC will set time correctly when using Thonny and connected to a computer and manually initiated
# otherwise clock will init to the wrong value of 2021-01-01 00:00:01
rtc = machine.RTC()
timestamp = rtc.datetime()
timestring = "%04d-%02d-%02d %02d:%02d:%02d" % (
    timestamp[0:3] + timestamp[4:7])

#establishing Temperature reading and conversion to degrees C for PIR sensor readings
sensorTemp = machine.ADC(machine.ADC.CORE_TEMP)
conversionFactor = 3.3/ (65535)
read = sensorTemp.read_u16() * conversionFactor
temp = 27 - (read - 0.706)/0.001721

print('Date and Time = ' + timestring)

#LED FOR PIR SENSOR
pirled = Pin(0,Pin.OUT)
#ASSIGNING PIR SENSOR PIN
pirsensor= Pin(3,Pin.IN)
#setting led to default to off in case of program break
pirled.value(0)
#creating text file to hold PIR sensor data readings
file = open ("PIRdata.txt", "w")
file.read()
file.write(timestring + ", temp: " + str(temp) + ' C ' + "\n")
file.close()

#led = Pin(0, Pin.OUT)
led = machine.Pin("LED", machine.Pin.OUT)

# LIGHT SENSOR
# GP27 -> ADC1, 5V
photo_sensor = ADC(1)
tilt_sensor = Pin(4, Pin.IN)
dhtSensor = DHT11(Pin(15, Pin.OUT, Pin.PULL_DOWN))

pircount=0
count = 0

# tilt variables
tilt = False
tilt_start = 0
buffer = deque((), 10)
majority = 0

# humidity variables
ShowerStartTime = 0
showerStarted = False
total_temp = 0
total_hum = 0
count = 0
humidity_threshold = 1000

while True:
    
    #Having the time refreshing constantly while the program is running for more accurate timestamps
    rtc = machine.RTC()
    timestamp = rtc.datetime()
    timestring="%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3] + timestamp[4:7])
    
    #PIR sensor code
    if PIRcount >=40:#20 is an arbritrary number that will be adjusted upon further tweaking
        pirled.value(1)
        print("Real interaction detected")
        file = open ("count.txt", "a")
        file.write("human detected. Temperature is " + str(temp) + " C° at " + str(timestring) + "\n" )
        file.close()
        PIRcount = 0
    if pirsensor.value()==0:
        pirled.value(0)
    else
        pirled.value(1)
        file = open ("PIRdata.txt", "a")
        file.write("human detected and the ambient temp is " + str(temp) + " at " + str(timestring) + "\n")
        file.close()
        PIRcount +=1
        led.value(0)
        
    
    # light code
    while (count < 51):
        print(photo_sensor.read_u16())
        sleep(2)  # set a delay between readings
        count += 1

    # tilt code
    if len(buffer) == 10:
        if not tilt:
            if majority >= 5:
                tilt = not tilt
                tilt_start = time.ticks_ms()

        if tilt:
            if majority < 5:
                tilt = not tilt
                print('took ', time.ticks_diff(
                    time.ticks_ms(), tilt_start)/1000, ' seconds to open')
                print('door opened')

        majority -= buffer.popleft()

    buffer.append(tilt_sensor.value())
    majority += tilt_sensor.value()

    # humidity code
    temp = dhtSensor.temperature
    hum = dhtSensor.humidity

    # calculate the average temparature and humidity for a neutral bathroom
    # stop calculating average if shower has started
    if not showerStarted:
        total_hum += hum
        total_temp += temp
        count += 1
        avg_hum = total_hum/count
        avg_temp = total_temp/count

    # if the shower has been started, get the initial time
    if not showerStarted and hum-avg_hum > humidity_threshold:
        ShowerStartTime = time.ticks_ms()
        ShowerStarted = True

    # if it has been more than hour after the start and the bathroom is still very humid, indicates an issue
    minutes = 60
    runtime = time.ticks_diff(
        time.ticks_ms(), ShowerStartTime)/60000
    if showerStarted and runtime >= minutes:
        if hum - avg_hum > humidity_threshold:
            print(f'ALERT: Shower has been running for {runtime} minutes')
        else:
            print(f'Shower ended: lasted {minutes} minutes')
            showerStarted = False

    # Can also keep track of how long showers are, if it ends before 60 minutes
    if showerStarted and hum-avg_hum < humidity_threshold:
        print(f'Shower ended: lasted {runtime} minutes')
        showerStarted = False

    # if it's been a week of data collection, save to log file and reset
    if count == 604800:
        file = open("humiditydata.txt", "w")
        file.read()
        file.write(timestring + ", temp: " + str(total_temp/count) +
                   ", " + "humidity: " + str(total_hum/count))
        file.close()
        total_temp = total_hum = count = 0

    # sleep
    sleep(0.1)
# Light Sensor showed a range of values when exposed to light of 3088 - 3312 and when no light 65535
