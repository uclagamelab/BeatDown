from time import sleep
import os
import RPi.GPIO as GPIO
import threading

class ButtonChecker(threading.Thread):
	def __init__(self, buttonPins = []):
		threading.Thread.__init__(self)
		self.buttonPins = buttonPins#[23, 24, 25, 4]
		self.buttonStates = [True] * len(self.buttonPins)
		GPIO.setmode(GPIO.BCM)
		for i in range(4):
			GPIO.setup(self.buttonPins[i], GPIO.IN)
		
		self.pressCallbacks = []
		self.releaseCallbacks = []

	def checkButtons(self):
		while True:
			for i in range(4):
				buttonState = GPIO.input(self.buttonPins[i])
				if ( buttonState == False and self.buttonStates[i] == True):
					for cb in self.pressCallbacks:
						cb(i)
					print 'press ' + str(i)
				
				elif ( buttonState == True and self.buttonStates[i] == False):
					for cb in self.releaseCallbacks:
						cb(i)
					print 'release ' + str(i)

				self.buttonStates[i] = buttonState

    	def addPressCallBack(self, callback):
		self.pressCallbacks.append(callback)

	def run(self):
       	    while True:
		    bc.checkButtons()
		    sleep(.05)


if __name__ == '__main__':
    print "go go button test"
    bc =  ButtonChecker([23, 24, 25, 4])
    bc.start()
