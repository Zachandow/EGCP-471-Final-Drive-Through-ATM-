#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins (distance sensor 1) Font
GPIO_TRIGGER = 13
GPIO_ECHO = 6
GPIO_FLAG = 17

#set Pins for disntace sensor 2 Heihgt
TRIGGER_UP = 26
ECHO_UP = 19
FLAG_UP = 27
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_FLAG, GPIO.OUT)

GPIO.setup(TRIGGER_UP, GPIO.OUT)
GPIO.setup(ECHO_UP, GPIO.IN)
GPIO.setup(FLAG_UP, GPIO.OUT)

GPIO.output(GPIO_FLAG, False)
GPIO.output(FLAG_UP, False)

def distance_V():
    # set Trigger to HIGH
    GPIO.output(TRIGGER_UP, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIGGER_UP, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(ECHO_UP) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(ECHO_UP) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance_up = (TimeElapsed * 34300) / 2
 
    return distance_up
def distance_H():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
