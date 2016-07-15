#!/usr/bin/python

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Jangho_Servo, Jangho_LED

# This class allows you to control robot in the low-level manner
# ControlTower class must use this class to control robot
class ProbeDevice:
	# constants fro convenient use
	DCMOTOR_FORWARD = 1
	DCMOTOR_BACKWARD = 2
	DCMOTOR_BRAKE = 3
	DCMOTOR_RELEASE = 4

	# 2 LED
	LEFT_LED = 5
	RIGHT_LED = 6

	# 2 servo motor
	SERVOMOTOR_HORIZONTAL = 7
	SERVOMOTOR_VERTICAL = 8

	def __init__(self):
		# motor HAT device init
		# address is 0x60, PWM Frequency = 50Hz
		self.mMotorHAT = Adafruit_MotorHAT(addr=0x60, freq=50)
		
		# Get left, right DC Motor
		self.mLeftDCMotor = self.mMotorHAT.getDCMotor(1)
		self.mRightDCMotor = self.mMotorHAT.getDCMotor(0)
		
		# Get left, right LED
		self.mLeftLED = self.mMotorHAT.getLED(0)
		self.mRightLED = self.mMotorHAT.getLED(1)

		# LED init brightness
		self.mLeftLED.setBrightness(255)
		self.mRightLED.setBrightness(255)

		# Get Two servo motors
		self.mHorizontalServoMotor = self.mMotorHAT.getServoMotor(0)
		self.mVerticalServoMotor = self.mMotorHAT.getServoMotor(1)

	def operateServoMotor(self, enumSide, numDutyCycle):
		# set the value of duty cycle of horizontal servo motor
		
		if enumSide == ProbeDevice.SERVOMOTOR_HORIZONTAL:
			self.mHorizontalServoMotor.setDutyCycle(numDutyCycle)

		elif enumSide == ProbeDevice.SERVOMOTOR_VERTICAL:
			self.mVerticalServoMotor.setDutyCycle(numDutyCycle)

	def turnOffMotors(self):
		# release all DC Motors
		self.mLeftDCMotor.run(Adafruit_MotorHAT.RELEASE)
		self.mRightDCMotor.run(Adafruit_MotorHAT.RELEASE)

	def operateDCMotors(self, leftMode, leftValue, rightMode, rightValue):
		# leftValue corresponds to the left DC Motor
		# leftMode corresponds to the direction of left DC Motor
		# rightValue corresponds to the right DC Motor
		# rightMode corresponds to the direction of right DC Motor
		self.mLeftDCMotor.setSpeed(leftValue)
		self.mRightDCMotor.setSpeed(rightValue)
		self.mLeftDCMotor.run(leftMode)
		self.mRightDCMotor.run(rightMode)

	def operateLED (self, direction, bOn):
		# bDirection == true -> LEFT LED
		# bDirection == false -> RIGHT LED
		if direction == ProbeDevice.LEFT_LED:
			if bOn == True:
				self.mLeftLED.runLED(Adafruit_MotorHAT.LED_ON)
			else:
				self.mLeftLED.runLED(Adafruit_MotorHAT.LED_OFF)
		else:
			if bOn == True:
				self.mRightLED.runLED(Adafruit_MotorHAT.LED_ON)
			else:
				self.mRightLED.runLED(Adafruit_MotorHAT.LED_OFF)

	def endUseDevice(self):
		turnOffMotors(self)		