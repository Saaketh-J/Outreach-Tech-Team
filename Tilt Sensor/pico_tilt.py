# This program is using the Raspberry Pi Pico to gather data using a simple tilt 
# This was written using MicroPython version 1.19.1

from machine import Pin
from time import sleep
# import a double ended queue data structure
from collections import deque
# importing the time library
import time

# Connect the Pico's GP1 to tilt sensor's DO pin.
# Connect the Pico's 3.3V Pin to PIR sensor's VCC pin.
# Connect the Pico's GND pin to PIR sensor's GND pin.
tilt_sensor = Pin(1 , Pin.IN)
        
        
# Experiments:

## Experiment 1: Determining when a door was opened:
    # no tilt -> tilt -> no tilt

# # variable to store the last tilt status
# tilt = False
#     
# while True:
#     # if it hasn't been tilted, but now is, start looking for when it will be reset again
#     if not tilt:
#         if tilt_sensor.value() == 1:
#             tilt = not tilt
#         sleep(0.2)
# 
#     # if it has been tilted but now resets, it means the door has been opened
#     if tilt:
#         if tilt_sensor.value() == 0:
#             tilt = not tilt
#             print('door opened')
#         sleep(0.2)

    # outcomes: succesful printing of accurate state
    # problems: prints "door opened" even when the sensor is tilted just a little and reset (not accurate representation of real world behavior)
    # improvement: has to be tilted for at least some time (2 seconds?)



# Experiment 2: Ignoring small disturbances (mis-detections) in tilt 
# Create a buffer (size 10) to collect tilt info and the majority status of the buffer becomes the actual tilt state at that time
    # buffer size and sleep time are negatively correlated for accurate responses

# buffer = deque((), 10)
# # variable to instantly see if the sensor has detected more of a tilt or a non-tilt status (replacement for 'sum(buffer)'
# majority = 0
# while True:
#     # only process if you've had at least 10 readings
#     if len(buffer) == 10:
#         # if there have been more tilt statuses, assume it is tilted
#         if majority >= 5:
#             print(buffer)
#             print('yes')
#         # if there have been more non-tilt statuses, assume it is not tilted
#         else:
#             print(buffer)
#             print('no')
#         # remove the first seen reading in the buffer and update majority accordingly
#         majority -= buffer.popleft()
#     # update with the current reading    
#     buffer.append(tilt_sensor.value())
#     majority += tilt_sensor.value()
#     sleep(0.1)

    #outcomes: Works as expected but not sure if this is significantly better than increasing the sleep time on experiment 1
    
    
# Experiment 3: Determine amount of time it takes to open and close/go through
# tilt = False
# #variable to hold the start time when sensor is first tilted
# start = 0
# 
# while True:
#     if not tilt:
#         if tilt_sensor.value() == 1:
#             tilt = not tilt
#             # store current time
#             start = time.ticks_ms()
#         sleep(0.2)
#     
#     if tilt:
#         if tilt_sensor.value() == 0:
#             tilt = not tilt
#             # subtract current time with the time when the sensor was tilted
#             # divide by 1000 because 'time.ticks_ms()' returns milliseconds
#             print('took ', time.ticks_diff(time.ticks_ms(), start)/1000, ' seconds to open')
#             print('door opened')
#             
#         sleep(0.2)
    
    # Outcomes: Works sometimes
    # Problems: Sensor mis-detects that the tilt has been reset while it is in a tilted position so the results are incorrect


# Experiment 4: Fix the problem in Exp3 by incorporating buffer solution from Exp2
tilt = False
start = 0


buffer = deque((), 10)
majority = 0
while True:
    if len(buffer) == 10:
        if not tilt:
            if majority >= 5:
                tilt = not tilt
                start = time.ticks_ms()
        
        if tilt:
            if majority < 5:
                tilt = not tilt
                print('took ', time.ticks_diff(time.ticks_ms(), start)/1000, ' seconds to open')
                print('door opened')
        
        majority -= buffer.popleft()
        
    buffer.append(tilt_sensor.value())
    majority += tilt_sensor.value()
    sleep(0.1)

    # Outcomes: Works much better than Exp3
    # Problems: False negatives occur (doesn't detect always detect door
    #           Doesn't always detect slow openings (sensitivity could be an issue)
