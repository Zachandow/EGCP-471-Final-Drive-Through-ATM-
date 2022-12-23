import RPi.GPIO as GPIO
import time
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
import atexit
from distanceReader import *
from HorizontalFunction import *
from SuperFinalATMFunction import *

# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(addr=0x6f)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
myMotor1 = mh.getMotor(3)
myMotor2 = mh.getMotor(1)
myMotor1.setSpeed(0)
myMotor2.setSpeed(0)	
	
GPIO.setmode(GPIO.BCM)
tmpD = 0
#myMotor.run(Raspi_MotorHAT.FORWARD)

GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
print('Starting Vertical Movement')
while True:
	while True:
		if(GPIO.input(23) == 0) and (GPIO.input(24) == 1):#to lower
			tmpD = distance_V()
			if(tmpD < 34):#36.5
				myMotor1.run(Raspi_MotorHAT.BACKWARD)
				myMotor1.setSpeed(255)
				GPIO.output(20, False)
				GPIO.output(21, False)			
			else:
				GPIO.output(20, True)
				GPIO.output(21, False)
				myMotor1.setSpeed(0)			
			#print('going one way')
		elif(GPIO.input(23) == 1) and (GPIO.input(24) == 0):# to higher
			tmpD = distance_V()
			if(tmpD > 6):#6		
				myMotor1.run(Raspi_MotorHAT.FORWARD)
				myMotor1.setSpeed(255)
				GPIO.output(20, False)
				GPIO.output(21, False)			
			else:
				GPIO.output(20, False)
				GPIO.output(21, True)
				myMotor1.setSpeed(0)			
			#print('or another')
		elif(GPIO.input(23) == 0) and (GPIO.input(24) == 0):
			tmpD = distance_V()
			myMotor1.setSpeed(0)
			GPIO.output(20, False)
			GPIO.output(21, False)		
			#print('doing nothing')
			
		elif(GPIO.input(23) == 1) and (GPIO.input(24) == 1):
			print('Exiting Vertical Movement')
			break
		print(GPIO.input(23) , GPIO.input(24),tmpD )
		time.sleep(.2)
		#print(GPIO.input(23), GPIO.input(24), tmpD)
		
	GPIO.output(20, True)
	GPIO.output(21, True)
	time.sleep(1)
	print('Starting Horizontal Movement')
	moveHorizontal()
	print('Ending Horizontal Movment')	
	print('Starting Vertical Movement')
	app()
	print('Done with with movement')
	print('Reseting')
	tmpD = distance_V()

	while (tmpD > 21):
		myMotor1.run(Raspi_MotorHAT.FORWARD)
		myMotor1.setSpeed(255)
		tmpD = distance_V()
		time.sleep(0.1)

	while (tmpD < 20):
		myMotor1.run(Raspi_MotorHAT.BACKWARD)
		myMotor1.setSpeed(255)
		tmpD = distance_V()
		time.sleep(0.1)

	myMotor1.setSpeed(0)
	myMotor2.run(Raspi_MotorHAT.FORWARD)
	myMotor2.setSpeed(255)
	time.sleep(40)
	turnOffMotors()	
	GPIO.output(20, False)
	GPIO.output(21, False)






