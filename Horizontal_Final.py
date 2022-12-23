import RPi.GPIO as GPIO
import time
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
import atexit
from distanceReader import *

# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(addr=0x6f)


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)


atexit.register(turnOffMotors)

horizontalMotor = mh.getMotor(1)

GPIO.setmode(GPIO.BCM)
tmpD = 0
counter = 0		#This counter is to make sure that we get 3 measurements of less than 6 cm before the motor stops. Protects against outlier measurements

GPIO.setup(16,GPIO.OUT)		#Flag that we can use to communicate with the adafruit breakout
GPIO.output(16, False)

while True:
	tmpD = distance_H()
    
	if (tmpD >= 6):										#If distance from car is greater than 6cm, run the motor
		horizontalMotor.run(Raspi_MotorHAT.BACKWARD)
		horizontalMotor.setSpeed(255)
		print (tmpD, counter)
		time.sleep(0.1)
        
	elif (tmpD < 6):		#If car distance is less than 6cm...
		counter += 1		#Increment the counter
		print (tmpD, counter)
		
		if (counter == 3):			#If the counter is equal to 3...
			turnOffMotors()			#We are done, turn off motors, set flag to True, then break from while loop
			GPIO.output(16, True)
			print ('Done!')
			break
               
	else:							#If something goes wrong, turn off motors, display error message, then break
		turnOffMotors()
		print('Error! I broke it')
		break

		
        
