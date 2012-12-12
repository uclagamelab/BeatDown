'''
Handles input and output from the pins of raspberry pi
'''

import RPi.GPIO as GPIO
from time import *
import threading

class RPiButtonChecker:
    def __init__( self, buttonPins, lightPins):
        self.buttonPins = buttonPins
#        self.lightPins = lightPins

        GPIO.setmode(GPIO.BCM)

        for i in range(len(self.buttonPins)):
            GPIO.setup(self.buttonPins[i], GPIO.IN)

        for pin in lightPins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
    

    def cleanup(self):
        GPIO.cleanup()
    
    def buttonPressed(self, idx):
        return GPIO.input(self.buttonPins[idx])
    
    def setLightOn(self, pin, on):
            GPIO.output(pin, on)
    
    def start(self):
        pass
