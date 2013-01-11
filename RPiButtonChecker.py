'''
Handles input and output from the pins of raspberry pi
'''

import RPi.GPIO as GPIO
from time import *
from InputChecker import *
import threading


class RPiButtonChecker(InputChecker):
    def __init__( self, buttonPins, lightPins):


        bPins = []
        lPins = []

        for playerPins in buttonPins:
            print playerPins[0]
            print playerPins[1]
            bPins.append(playerPins[0])
            bPins.append(playerPins[1])

        for playerPins in lightPins:
            lPins.append(playerPins[0])
            lPins.append(playerPins[1])

        InputChecker.__init__(self, bPins, lPins)
        self.buttonPins = buttonPins
#        self.lightPins = lightPins

        GPIO.setmode(GPIO.BCM)

        for playerPins in buttonPins:
            for pin in playerPins:
                GPIO.setup(pin, GPIO.IN)

        for playerPins in lightPins:
            for pin in playerPins:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, False)
    
    
    def buttonPressed(self, pin):
        return GPIO.input(pin)#(self.buttonPins[idx])
    
    def setLightOn(self, pin, on):
        #print(str(pin) + " " + str(on))
        GPIO.output(pin, on)
    
    def start(self):
        pass
