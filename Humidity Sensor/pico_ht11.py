# This program is using the Raspberry Pi Pico to gather data using a simple tilt
# This was written using MicroPython version 1.19.1

from sympy import terms_gcd
from machine import Pin
from dht import DHT11, InvalidChecksum
import time


# Timestamp class RTC will set time correctly when using Thonny and connected to a computer and manually initiated
# otherwise clock will init to the wrong value of 2021-01-01 00:00:01
rtc = machine.RTC()
timestamp = rtc.datetime()
timestring = "%04d-%02d-%02d %02d:%02d:%02d" % (
    timestamp[0:3] + timestamp[4:7])

print('Date and Time = ' + timestring)


# Code to write data to file
# file = open("sensordata.txt", "w")
# file.read()
# file.write(timestring + ", temp: " + str(readLight(photoPIN)) + "%")
# file.close()

# Connect the Pico's GP1 to ht11 sensor's DAT pin.
# Connect the Pico's 3.3V Pin to ht11 sensor's VCC pin.
# Connect the Pico's GND pin to ht11 sensor's GND pin.
dhtPIN = 3
dhtSensor = DHT11(Pin(dhtPIN, Pin.OUT, Pin.PULL_DOWN))

# Print the temperature followed by the humidity
# while True:
#     print("Temp: {}°C".format(dhtSensor.temperature),
#           "| Hum: {0:.1%}".format(dhtSensor.humidity/100))
#     time.sleep(1.1)

# # Experiment 1: Determine when there has been a major shift in humidity/temperature -> indicative of a shower taking place
# # store running mean and number of terms so far
# avg_humidity = dhtSensor.temperature
# avg_temperature = dhtSensor.humidity
# terms = 0

# while True:
#     temp = dhtSensor.temperature
#     hum = dhtSensor.humidity
#     # temperature might not be the best indicator for a shower
#     # if current temperature is 5 degree C hotter, temperature is unusually high
#     if temp-avg_temperature > 5:
#         print('Temperature unusually high')
#     # if humidity changes by more than 10%, there is likely a shower taking place
#     if hum-avg_humidity > 1000:
#         print('Shower running')

#     # store a running mean
#     avg_humidity += (hum-avg_humidity)/terms
#     terms += 1

#     time.sleep(60)


# # Experiment 2: Determine if a shower has been running on for too long -> indicates a potential fall or other issue
ShowerStartTime = 0
# semaphore to block checking for start time after a shower's been started
showerStarted = False
# example avg_temp and avg_hum
total_temp = 0
total_hum = 0
count = 0
humidity_threshold = 1000
while True:
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
