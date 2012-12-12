import time, threading, os
from NotePattern import *
from Tkinter import *
import random
import math
from InputChecker import *
from KeyChecker import *

class NoteModifiers:
    MISSLAP = 0
    GOODSLAP = 1
    NONE = 2

class SynthController:
    
    QNOTE_DELAY = .4
    
    #SLAP_KEYS = [['j', 'k'], ['a', 's']]
    
    LIGHT_PINS = [[18, 10], [22, 17]]
    SLAP_KEYS = [[23, 24], [25, 4]]
    HIP_KEYS = ['z', 'm']
    QUIT_KEY = 'Escape'
    
    def __init__(self):
        
        self.stopAllNotes()
        
        self.qtrNoteDuration = self.QNOTE_DELAY
        self.pattern = NotePattern()
        self.ticksUntilSlap = 1
        self.ticksUntilSlapCtr = 0
        self.quitNow = False
        
        self.previousNotes = []
    
        self.slapCallback = None
        self.hipButtonCallback = None
    
        self.lastSlappedPlayer = 0
        self.lastSlappedButton = 0
    
        
        self.inputChecker = InputChecker([23, 24, 25, 4], [18, 22, 10, 17])#(['j', 'k' ,'a', 's', 'z', 'm', 'Escape'])

        self.inputChecker.addPressCallback(self.inputPressCallback)
        self.inputChecker.addReleaseCallback(self.inputReleaseCallback)

        self.debugWindow = KeyChecker([])#self.inputChecker.buttonChecker
    
    '''
    enumerate the slap situations
    '''
    
    '''
    turn on 1 light, player slaps the light
    '''
    def triggerSinglePlayerSlap(self, targetPlayer, targetButton):

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
                    pass
                
                # turn all the lights off
                for i in range(2):
                    for j in range(2):
                        self.setLightOn(i, j, False)
                        
                self.slapCallback = None
                
                self.ticksUntilSlap = random.randint(1, 2)
                self.ticksUntilSlapCtr = 0
                self.qtrNoteDuration = self.QNOTE_DELAY
                self.update(noteModifier)
            else:
                pass #wrong player slaps! ignore for now
        
        self.slapCallback = tempSlapCallBack
    
    def triggerPlayerRace(self, idx1, idx2):
        pass
    
    
    def update(self, noteModifier=NoteModifiers.NONE):
        #not especially thread safe
        if self.quitNow:
            return
                
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
            threading.Timer(self.qtrNoteDuration, self.update).start()

        else:#last note of run

            changePlayerRoll = random.randint(0,1)
            buttonIdx = random.randint(0,1)
            
            nextSlappedPlayer = self.lastSlappedPlayer
            if changePlayerRoll > 0: #switch player most of the time
                nextSlappedPlayer = (self.lastSlappedPlayer + 1) % 2

            if nextSlappedPlayer == self.lastSlappedPlayer and buttonIdx == self.lastSlappedButton:
                def f(): self.triggerSinglePlayerSlap(nextSlappedPlayer, buttonIdx)
                threading.Timer(self.qtrNoteDuration * .75, f).start()
            else:
                self.triggerSinglePlayerSlap(nextSlappedPlayer, buttonIdx)

            self.lastSlappedPlayer = nextSlappedPlayer
            self.lastSlappedButton = buttonIdx
                
    def setLightOn(self, player, side, on):
        self.debugWindow.setLightOn(player, side, on)
        self.inputChecker.setLightOn(self.LIGHT_PINS[player][side], on)

    def noteOn(self, midiNum):
        os.system("echo '0 " + str(midiNum) + " 120;' | pdsend 3001")

    def noteOff(self, midiNum):
        os.system("echo '0 " + str(midiNum) + " 0;' | pdsend 3001")

    def hipButtonPress(self, player = None, buttonIdx = None):
        self.debugWindow.hipButtonPress(player, buttonIdx, True)

    def hipButtonRelease(self, player = None, buttonIdx = None):
        self.debugWindow.hipButtonPress(player, buttonIdx, False)
    
    def inputPressCallback(self, buttonPin):
        if buttonPin == self.QUIT_KEY:
            self.quit()
        
        for i in range(2):
            if buttonPin == SynthController.HIP_KEYS[i]:
                self.hipButtonPress(i)
            
            for j in range(2):
                if buttonPin == SynthController.SLAP_KEYS[i][j]:
                    self.slapPress(i, j)

    def inputReleaseCallback(self, buttonPin):
        for i in range(2):
            if buttonPin == SynthController.HIP_KEYS[i]:
                self.hipButtonRelease(i)
            
            for j in range(2):
                if buttonPin == SynthController.SLAP_KEYS[i][j]:
                    self.slapRelease(i, j)

    def slapPress(self, playerIdx, buttonIdx): #player = person getting slapped, button = button they slapped
        
        #outline box, for pc development
        self.debugWindow.slapPress(playerIdx, buttonIdx, True)

        if self.slapCallback != None:
            self.slapCallback(playerIdx, buttonIdx)

    def slapRelease(self, playerIdx, buttonIdx):
        self.debugWindow.slapPress(playerIdx, buttonIdx, False)
    
    def getOpponentIdx(self, playerIdx):
        if playerIdx == 0:
            return 1
        else:
            return 0

    def stopAllNotes(self):
        os.system("echo '1 0;' | pdsend 3001") # stop all notes

    def quit(self):
        self.stopAllNotes()
        self.quitNow = True
        self.debugWindow.quit()
        sys.exit(0)


if __name__ == "__main__":
    print "Go"
    synthCon = SynthController()
    synthCon.inputChecker.start()
    synthCon.update()
    synthCon.debugWindow.start()
    
