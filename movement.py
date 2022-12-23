import RPi.GPIO as GPIO
import time
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from HorizontalFunction import *
import atexit


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
V_motor = mh.getMotor(3)
H_motor = mh.getMotor(1)
V_motor.setSpeed(0)
H_motor.setSpeed(0)	
	
GPIO.setmode(GPIO.BCM)

moveHorizontal()
#myMotor.run(Raspi_MotorHAT.FORWARD)

#H_motor.run(Raspi_MotorHAT.FORWARD)
#H_motor.setSpeed(255)

#H_motor.run(Raspi_MotorHAT.BACKWARD)
#H_motor.setSpeed(255)

#V_motor.run(Raspi_MotorHAT.FORWARD)
#V_motor.setSpeed(255)

#V_motor.run(Raspi_MotorHAT.BACKWARD)
#V_motor.setSpeed(255)


#time.sleep(30)
#V_motor.setSpeed(0)
#H_motor.setSpeed(0)
			



