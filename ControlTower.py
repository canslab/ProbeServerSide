from ProbeDevice import ProbeDevice
import time

class ControlTower:

	def __init__(self, robotDevice):
		# ControlTower has a robot device, 
		# after you receive the json command, you should parse that string,
		# and make robot work using the specified command 
		self.mRobotDevice = robotDevice
		
	def processJSON(self, strJSONdata):
		# Process JSON string from the client 
		# First it identifies the target device 
		# ex.) LED ==> "TARGET" is "LED"
		#
		# after that, this function calls appropriate methods to process respectively.
		if strJSONdata["Target"] == "LED":
			self.processLEDJob(strJSONdata)
		elif strJSONdata["Target"] == "DCMotors":
			self.processDCMotorJob(strJSONdata)
		elif strJSONdata["Target"] == "ServoMotors":
			self.processServoMotorJob(strJSONdata)

	def processServoMotorJob(self, strJSONdata):
		# Process Servo Motor related Jobs
		# [Format Example]
		# {"Target":"ServoMotors", { 0:"Horizontal", 2:#(dutyCycle) }}
		strSide = strJSONdata["Params"][0]
		numDutyCycle = strJSONdata["Params"][1]

		# if the first parameter is equal to "Horizontal", it means you should control bottom servo mottor(horizontal servo motor)
		# otherwise, it means the upper servo motor(vertical servo motor)
		if strSide == "Horizontal":
			self.mRobotDevice.operateServoMotor(ProbeDevice.SERVOMOTOR_HORIZONTAL, numDutyCycle)
		elif strSide == "Vertical":
			self.mRobotDevice.operateServoMotor(ProbeDevice.SERVOMOTOR_VERTICAL, numDutyCycle)

	def processLEDJob(self, strJSONdata):
		# Process LED related Jobs
		# strJSONdata Form ==>  "TARGET" = "LED", "SIDE" = "LEFT", "VALUE" = "ON"
		if strJSONdata["Params"][0] == "Left":
			if strJSONdata["Params"][1] == 1:
				self.mRobotDevice.operateLED(direction=ProbeDevice.LEFT_LED, bOn=True)
			elif strJSONdata["Params"][1] == 0:
				self.mRobotDevice.operateLED(direction=ProbeDevice.LEFT_LED, bOn=False)

		elif strJSONdata["Params"][0] == "Right":
			if strJSONdata["Params"][1] == 1:
				self.mRobotDevice.operateLED(direction=ProbeDevice.RIGHT_LED, bOn=True)
			elif strJSONdata["Params"][1] == 0:
				self.mRobotDevice.operateLED(direction=ProbeDevice.RIGHT_LED, bOn=False)

	def processDCMotorJob(self, strJSONdata):
		# this function interpret JSON string command and
		# does work.
		leftMode = self.__convertDCMotorModeStringToEnum(strJSONdata["Params"][0])
		rightMode = self.__convertDCMotorModeStringToEnum(strJSONdata["Params"][2])
		
		leftValue = strJSONdata["Params"][1]
		rightValue = strJSONdata["Params"][3]

		self.mRobotDevice.operateDCMotors(leftMode, leftValue, rightMode, rightValue)	
		
		# in order to run motors only for 0.05 seconds.
		# if this function is not called, DC motors would run forever.. 
		time.sleep(0.1)

	def __convertDCMotorModeStringToEnum(self, strToBeConverted):
		# strToBeConverted ---> one of enum type
		if strToBeConverted == "Forward":
			return ProbeDevice.DCMOTOR_FORWARD
		elif strToBeConverted == "Backward":
			return ProbeDevice.DCMOTOR_BACKWARD
		elif strToBeConverted == "Break":
			return ProbeDevice.DCMOTOR_BRAKE
		elif strToBeConverted == "Release":
			return ProbeDevice.DCMOTOR_RELEASE
