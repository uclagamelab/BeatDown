import RPi.GPIO as GPIO
from time import *
import threading

class RPiButtonChecker:
    def __init__( self, buttonPins):
        self.buttonPins = buttonPins
        GPIO.setmode(GPIO.BCM)
        for i in range(len(self.buttonPins)):
            GPIO.setup(self.buttonPins[i], GPIO.IN)
    
    
    def buttonPressed(self, idx):
        return GPIO.input(self.buttonPins[idx])
    
    def start(self):
        pass