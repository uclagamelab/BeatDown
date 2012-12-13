import time, threading, os
from NotePattern import *
from Tkinter import *
import random
import math
from InputChecker import *

USE_KEYBOARD = True

if USE_KEYBOARD:
    from KeyChecker import *
else:
    from RPiButtonChecker import *

class NoteModifiers:
    MISSLAP = 0
    GOODSLAP = 1
    NONE = 2

class SynthEvent:
    def __init__(self, function, delay):
        self.delay = delay
        self.function = function

    def update(self):
        self.delay = self.delay - 1

    def isReady(self):
        return self.delay <= 0

    def execute(self):
        self.function()


class SynthController:#(threading.Thread):
    QNOTE_DELAY = .4
    TICK_DELAY = .01
    
    # this system is really dumb
    # probably want to register what the callback should return?
    # have slightly different callback for each pin?
    LIGHT_PINS = [[18, 10], [22, 17]]
    
    
    SLAP_KEYS = [[23, 24], [25, 4]]
    HIP_KEYS = []
    if USE_KEYBOARD:
        SLAP_KEYS = [['j', 'k'] ,['a', 's']]
        HIP_KEYS = ['z', 'm']
    
    QUIT_KEY = 'Escape'
    
    def __init__(self):
        #threading.Thread.__init__(self) # should be able to ditch eventually
        self.stopAllNotes()
        
        self.qtrNoteDuration = self.QNOTE_DELAY
        self.pattern = NotePattern()
        self.quitNow = False
        
        self.previousNotes = []
    
        self.slapCallback = None
        self.hipButtonCallback = None
    
        self.lastSlappedPlayer = 0
        self.lastSlappedButton = 0
        
        self.ticksUntilSlap = 1
        self.ticksUntilSlapCtr = 0
    
        #self.inputChecker = InputChecker([23, 24, 25, 4], [18, 22, 10, 17])#(['j', 'k' ,'a', 's', 'z', 'm', 'Escape'])

        self.inputChecker = None
        if USE_KEYBOARD:
            self.inputChecker = KeyChecker(self.SLAP_KEYS, self.HIP_KEYS, self.LIGHT_PINS)
        else:
            self.inputChecker = RPiButtonChecker(self.SLAP_KEYS, self.LIGHT_PINS)

        
        self.inputChecker.addPressCallback(self.inputPressCallback)
        self.inputChecker.addReleaseCallback(self.inputReleaseCallback)
    
        self.events = []
        self.events.append(SynthEvent(self.setupNextNote, 0))
    
    '''
    enumerate the slap situations
    '''
    
    '''
    turn on 1 light, player slaps the light
    '''
    def triggerSinglePlayerSlap(self, targetPlayer, targetButton):

        print "trigger slap"
        #must store, because they will get clobbered after, and can't be relied upon in the callback
        
        self.setLightOn(targetPlayer, targetButton, True)
        
        def tempSlapCallBack(player, button):
            noteModifier = NoteModifiers.NONE
            if (player == targetPlayer):
                
                #trigger the note stretch and slap sfx in PD
                os.system("echo '2 0;' | pdsend 3001")
                if (button == targetButton):
                    #print "success!"
                    pass
                else:
                    noteModifier = NoteModifiers.MISSLAP
                    #print "mis-slap"
                    #pass
                
                print "temp slap callback"
                # turn all the lights off
                for i in range(2):
                    for j in range(2):
                        self.setLightOn(i, j, False)
                        
                self.slapCallback = None
                
                self.ticksUntilSlap = random.randint(1, 2)
                self.ticksUntilSlapCtr = 0
                self.qtrNoteDuration = self.QNOTE_DELAY
                self.setupNextNote(noteModifier)
            else:
                pass #wrong player slaps! ignore for now
        
        self.slapCallback = tempSlapCallBack
    
    def triggerPlayerRace(self, idx1, idx2):
        pass
    
    
    def update(self):
        toDelete = []
        for event in self.events:
            if event.isReady():
                event.execute()
                toDelete.append(event)
            else:
                event.update()
    
        for event in toDelete:
            self.events.remove(event)
    
                
    def setupNextNote(self, noteModifier=NoteModifiers.NONE):
        constTempoCutoff =  int(math.ceil(self.ticksUntilSlap * .8))

        if self.ticksUntilSlapCtr >= constTempoCutoff:
            nTempoChangeTicks = self.ticksUntilSlap - constTempoCutoff
            
            i = (1.0 * self.ticksUntilSlapCtr - constTempoCutoff) / (nTempoChangeTicks)
            self.qtrNoteDuration = pow(1 + i, 3) * self.QNOTE_DELAY
                

        self.ticksUntilSlapCtr = min(self.ticksUntilSlap, self.ticksUntilSlapCtr + 1)
        
        
        for note in self.previousNotes:
            self.noteOff(note)

        self.pattern.tick()
        currentNote = self.pattern.getCurrentNote()

        self.previousNotes = []
    
        if noteModifier == NoteModifiers.MISSLAP:
            if currentNote == NotePattern.REST:
                currentNote = -10 #if mess up on rest play rumbly low nonsense
            
            dissonantNote = currentNote - 1
            currentNote = currentNote + .25
            self.noteOn(dissonantNote)
            self.previousNotes.append(dissonantNote)

        if currentNote != NotePattern.REST:
            self.noteOn(currentNote)
            self.previousNotes.append(currentNote)

        if (self.ticksUntilSlapCtr < self.ticksUntilSlap - 1): #pattern not over
            delay = int(self.self.qtrNoteDuration / self.TICK_DELAY)
            self.events.append(SynthEvent(self.setupNextNote, delay))
            #threading.Timer(self.qtrNoteDuration, self.update).start()

        else:#last note of run

            changePlayerRoll = random.randint(0,1)
            buttonIdx = random.randint(0,1)
            
            nextSlappedPlayer = self.lastSlappedPlayer
            if changePlayerRoll > 0: #switch player most of the time
                nextSlappedPlayer = (self.lastSlappedPlayer + 1) % 2

            if nextSlappedPlayer == self.lastSlappedPlayer and buttonIdx == self.lastSlappedButton:
                def f(): self.triggerSinglePlayerSlap(nextSlappedPlayer, buttonIdx)
                delay = int(self.qtrNoteDuration * .75 / self.TICK_DELAY)
                self.events.append(SynthEvent(f, delay))
                #threading.Timer(self.qtrNoteDuration * .75, f).start()
            else:
                self.triggerSinglePlayerSlap(nextSlappedPlayer, buttonIdx)

            self.lastSlappedPlayer = nextSlappedPlayer
            self.lastSlappedButton = buttonIdx
                
    def setLightOn(self, player, side, on):
        #self.debugWindow.setLightOn(player, side, on)
        print "syn " + str(self.LIGHT_PINS[player][side]) + " " + str(on)
        self.inputChecker.setLightOn(self.LIGHT_PINS[player][side], on)

    def noteOn(self, midiNum):
        #pass
        os.system("echo '0 " + str(midiNum) + " 120;' | pdsend 3001")

    def noteOff(self, midiNum):
        #pass
        os.system("echo '0 " + str(midiNum) + " 0;' | pdsend 3001")

    def hipButtonPress(self, player = None, buttonIdx = None):
        pass

    def hipButtonRelease(self, player = None, buttonIdx = None):
        pass
    
    def inputPressCallback(self, buttonPin):
        
        print("callback " + str(buttonPin))

        if buttonPin == self.QUIT_KEY:
            self.quit()
        
        for pins in SynthController.HIP_KEYS:
            for pin in pins:
                if pin == buttonPin:
                    self.hipButtonPress(pin)
            
        for i in range(len(self.SLAP_KEYS)):
            for j in range(len(self.SLAP_KEYS[i])):
                if buttonPin == SynthController.SLAP_KEYS[i][j]:
                    self.slapPress(i, j)

    def inputReleaseCallback(self, buttonPin):
        for i in range(len(SynthController.HIP_KEYS)):
            if buttonPin == SynthController.HIP_KEYS[i]:
                self.hipButtonRelease(i)
            
            for j in range(2):
                if buttonPin == SynthController.SLAP_KEYS[i][j]:
                    self.slapRelease(i, j)

    def slapPress(self, playerIdx, buttonIdx): #player = person getting slapped, button = button they slapped
    
        if self.slapCallback != None:
            self.slapCallback(playerIdx, buttonIdx)

    def slapRelease(self, playerIdx, buttonIdx):
        pass
    
    def getOpponentIdx(self, playerIdx):
        if playerIdx == 0:
            return 1
        else:
            return 0

    def stopAllNotes(self):
        #pass
        os.system("echo '1 0;' | pdsend 3001") # stop all notes

    def quit(self):
        print "synth con quit"
        self.stopAllNotes()
        self.quitNow = True
        sys.exit(0)

    def updateLoop(self):
        while True:
            self.inputChecker.checkButtons()
            self.update()
            #called modified update
            sleep(SynthController.TICK_DELAY)

    def start(self):#run(self):
        
        if USE_KEYBOARD:
            threading.Timer(10, self.updateLoop).start()
            self.inputChecker.start()
        else:
            self.updateLoop()
            

if __name__ == "__main__": 
    synthCon = SynthController()
    try:
        print "to update"
        synthCon.start()

    except KeyboardInterrupt:
        pass
    finally:
        synthCon.stopAllNotes()

