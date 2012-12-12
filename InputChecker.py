'''
    Generic button checking script can check either arduino pins or keyboard
    Also handles light on/off messages from SynthController
    '''
from time import sleep
import os
import threading
from KeyChecker import *
from RPiButtonChecker import *

class InputChecker(threading.Thread):
    def __init__(self, buttonPins, lightPins):
        threading.Thread.__init__(self)

        #self.buttonChecker = KeyChecker(buttonPins)
        self.buttonChecker = RPiButtonChecker(buttonPins, lightPins)

        self.buttonPins = buttonPins
        self.buttonStates = [True] * len(buttonPins)
        self.releaseCallbacks = []
        self.pressCallbacks = []

    def setLightOn(self, pin, on):
        self.buttonChecker.setLightOn(pin, on)

    def checkButtons(self):
        for i in range(len(self.buttonStates)):
            buttonState = self.buttonChecker.buttonPressed(i)#GPIO.input(self.buttonPins[i])
            buttonPin = self.buttonPins[i]
            if ( buttonState == False and self.buttonStates[i] == True):
                for cb in self.pressCallbacks:
                    cb(buttonPin)
            #print 'press ' + str(i)
        
            elif ( buttonState == True and self.buttonStates[i] == False):
                for cb in self.releaseCallbacks:
                    cb(buttonPin)
        #print 'release ' + str(i)
    
            self.buttonStates[i] = buttonState

    def addPressCallback(self, callback):
        self.pressCallbacks.append(callback)
    
    def addReleaseCallback(self, callback):
        self.releaseCallbacks.append(callback)
        
    def run(self):
        print "GOGOGOGO"
        while True:
            self.checkButtons()
            sleep(.05)


'''
if __name__ == '__main__':
    print "go go button test"
    bc =  InputChecker(['a', 's', 'j', 'k'])#([23, 24, 25, 4])
    
    def buttonCallback(i):
        if i == 0:
            print "YA"
        else:
            print "HOO"

    bc.addPressCallBack(buttonCallback)
    bc.start()
    bc.buttonChecker.start() # must call here because Tkinter needs to be started within parent thread
    '''
