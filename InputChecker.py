'''
    Generic button checking script can check either arduino pins or keyboard
    Also handles light on/off messages from SynthController
    '''
from time import sleep
import os
import threading

class InputChecker():
    def __init__(self, buttonPins, lightPins):
        self.buttonStates = dict()
        
        for buttonPin in buttonPins:
            self.buttonStates[buttonPin] = True # True when not pressed, for some reason
        
        self.releaseCallbacks = []
        self.pressCallbacks = []
        self.quitNow = False

    def cleanup(self):
        pass
        #self.buttonChecker.cleanup()

    def setLightOn(self, pin, on):
        raise NotImplementedError("need to implement!")
    
    def buttonPressed(self, pin):
        raise NotImplementedError("need to implement!")

    def checkButtons(self):
        for buttonPin in self.buttonStates.keys():
            buttonState = self.buttonPressed(buttonPin)#GPIO.input(self.buttonPins[i])
            
            if ( buttonState == False and self.buttonStates[buttonPin] == True):
                for cb in self.pressCallbacks:
                    cb(buttonPin)
            #print 'press ' + str(i)
        
            elif ( buttonState == True and self.buttonStates[buttonPin] == False):
                for cb in self.releaseCallbacks:
                    cb(buttonPin)
            #print 'release ' + str(i)
    
            self.buttonStates[buttonPin] = buttonState

    def addPressCallback(self, callback):
        self.pressCallbacks.append(callback)
    
    def addReleaseCallback(self, callback):
        self.releaseCallbacks.append(callback)

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
