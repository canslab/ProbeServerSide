import sys
from socket import *
from struct import *
import json
import time
import atexit
import ProbeDevice
import ControlTower

# make listenable socket... 
# it listens from all its IP address.... 
def makeListenableSocket(strIPAddress, nPortNumber):
	retSocket = socket(AF_INET, SOCK_STREAM)
	retSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	retSocket.bind((strIPAddress, nPortNumber))
	retSocket.listen(1)
	return retSocket

# main function 
if __name__ == '__main__':
	if len(sys.argv) == 1:
		print('your IP address, port number needed as arguments')
		sys.exit()

	strIPAddress = str(sys.argv[1])
	nPortNumber = int(sys.argv[2])

	print('Probe Server Program Started........')

	# make listenable socket using IP Address, Port Number
	serverSocket = makeListenableSocket(strIPAddress, nPortNumber)

	print('waiting acception')
	# After this statement, you can communicate with 
	# PC program using clientSocket
	# The address of client is obtained by clientAddress
	clientSocket, clientAddress = serverSocket.accept()
	print('client is ')
	print(clientAddress)

	print('communication start!!')

	# init robot device
	robotDevice = ProbeDevice.ProbeDevice()

	# make control tower to control robot
	controlTower = ControlTower.ControlTower(robotDevice)

	while True:
		# read 4 byte
		rb = clientSocket.recv(4)

		# it means socket has been closed, so while loop should be expired.
		if (rb == ''):
			print('connection broken...')
			sys.exit(-1)
			break;

		# get the number of the json data
		nLengthOfData = unpack('i', rb)[0]

		# receive JSON data up to nLengthOfData
		nBytesRead = 0
		strUnparsedJSONData = ""
		while nBytesRead < nLengthOfData:
			strRecvString = clientSocket.recv(nLengthOfData - nBytesRead)
			
			if strRecvString == '':
				print('socket connection broken')
				sys.exit(-1)

			nBytesRead = nBytesRead + len(strRecvString)
			strUnparsedJSONData = strUnparsedJSONData + strRecvString

		strParsedJSONData = json.loads(strUnparsedJSONData)

		# received command 
		print(strParsedJSONData)
		
		# interpret json data, and follows the interpreted command.
		controlTower.processJSON(strParsedJSONData)
		
		# 0.1 second rest..
		# time.sleep(0.2)
		robotDevice.turnOffMotors()		

	# close socket.
	clientSocket.close()
	robotDevice.endUseDevice()