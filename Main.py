import cv2
import time
import board
import digitalio
from camfunc import *
gpio0 = digitalio.DigitalInOut(board.C0) # 0 and 1 are comunications to the Pi
gpio0.direction = digitalio.Direction.OUTPUT
gpio1 = digitalio.DigitalInOut(board.C1)
gpio1.direction = digitalio.Direction.OUTPUT
gpio2 = digitalio.DigitalInOut(board.C2)
gpio2.direction = digitalio.Direction.INPUT# 2 and 3 and comunications from the Pi
gpio3 = digitalio.DigitalInOut(board.C3)
gpio3.direction = digitalio.Direction.INPUT
#Above is libraries and stuff

while True:
    camfunc() #calling the facial detection function
    time.sleep(3)
    gpio0.value = False# telling the pi we are done and will wait
    gpio1.value = False

    while (gpio2.value == 1) and (gpio3.value == 1):# waiting for the Pi to change from 11 to 00, meaning everything is reset and good to go again.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    


