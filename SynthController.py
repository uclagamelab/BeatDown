import time, threading, os
from NotePattern import *
from Tkinter import *
import random
import math

class NoteModifiers:
    MISSLAP = 0
    GOODSLAP = 1
    NONE = 2

class SynthController( Frame ):
    
    QNOTE_DELAY = .4
    
    SLAP_KEYS = [['j', 'k'], ['a', 's']]
    HIP_KEYS = ['z', 'm']
    
    def __init__(self):
        
        self.stopAllNotes()
        
        self.qtrNoteDuration = self.QNOTE_DELAY
        self.pattern = NotePattern()
        self.ticksUntilSlap = 1
        self.ticksUntilSlapCtr = 0
        self.quitNow = False
        
        self.previousNotes = []
    
    ## TKINTER BUSINESS
        Frame.__init__( self )
        self.pack( expand = YES, fill = BOTH )
        self.master.title( "BeetDaun Dbg." )
        self.master.geometry( "640x480" )
        
        self.canvas = Canvas(self, width=640, height=480)
        self.canvas.pack()
        
        #self.message1 = StringVar()
        #self.line1 = Label( self, textvariable = self.message1 )
        #self.message1.set( "Type any key or shift" )
        #self.line1.pack()
        
        #self.message2 = StringVar()
        #self.line2 = Label( self, textvariable = self.message2 )
        #self.message2.set( "" )
        #self.line2.pack()
        
        self.master.bind( "<Key>", self.keyPressed )
        self.master.bind( "<KeyRelease>", self.keyReleased )
        
        self.keysPressed = set()
        self.lightGfx = [[None, None], [None, None]]
        
        self.hipButtonGfx = [None, None]
    
        boxw = 50
        boxh = 50
        gapx = 25
        gapy = 200
        
        sx = 100
        sy = 100

        #slap buttons
        dx = 0
        dy = 0

        self.lightGfx[0][0] = self.canvas.create_rectangle( \
                                                           sx + dx, \
                                                           sy + dy, \
                                                           sy + boxw + dx, \
                                                           sy + boxh + dy,  \
                                                           fill="")
    
        dx = boxw + gapx
        dy = 0
        self.lightGfx[0][1] = self.canvas.create_rectangle( \
                                                               sx + dx, \
                                                               sy + dy, \
                                                               sy + boxw + dx, \
                                                               sy + boxh + dy,  \
                                                           fill="")
        
        #hip hold button
        dx = 2*boxw + 2*gapx
        dy = 0
        self.hipButtonGfx[0] = self.canvas.create_oval( \
                                                           sx + dx, \
                                                           sy + dy, \
                                                           sy + boxw + dx, \
                                                           sy + boxh + dy,  \
                                                           fill="")
    
        dx = 0
        dy = boxh + gapy
        self.lightGfx[1][0] = self.canvas.create_rectangle( \
                                                           sx + dx, \
                                                           sy + dy, \
                                                           sy + boxw + dx, \
                                                           sy + boxh + dy,  \
                                                           fill="")
        dx = boxw + gapx
        dy = boxh + gapy
        self.lightGfx[1][1] = self.canvas.create_rectangle( \
                                                           sx + dx, \
                                                           sy + dy, \
                                                           sy + boxw + dx, \
                                                           sy + boxh + dy,  \
                                                           fill="")
        
        #hip hold button
        dx = 2*boxw + 2*gapx
        dy = boxh + gapy
        self.hipButtonGfx[1] = self.canvas.create_oval( \
                                                     sx + dx, \
                                                     sy + dy, \
                                                     sy + boxw + dx, \
                                                     sy + boxh + dy,  \
                                                     fill="")
    
        #self.lightGfx[0][1] = self.canvas.create_rectangle(sx + boxw + gap, sy, sx + 2*boxw + gap, sy + boxh,  fill="")
    
        #self.lightGfx[1][0] = self.canvas.create_rectangle(sx, sy, sx + boxw, sy + boxh,  fill="")
        #self.lightGfx[1][1] = self.canvas.create_rectangle(sx + boxw + gap, sy, sx + 2*boxw + gap, sy + boxh,  fill="")
        #self.lightGfx[0][1] = self.canvas.create_rectangle(sx, sy, 150, 150, fill="")
    
    #self.waitingForSlap = False
    
    #self.currentNote = self.pattern.getCurrentNote()

        self.pack()
        self.slapCallback = None
        self.hipButtonCallback = None
    
        self.lastSlappedPlayer = 0
        self.lastSlappedButton = 0
    
    '''
    enumerate the slap situations
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
    
    #def singlePlayerSlapCallback(self):
    #pass
    
    def triggerPlayerRace(self, idx1, idx2):
        pass
    
    #def playerRaceSlapCallback(self):
    #pass
    
    def slapUpdate(self):
        pass
    def misslapUpdate(self):
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
        if (on):
            #self.lightGfx[player][side] = self.canvas.create_rectangle(50, 50, 150, 150, fill="red")
            self.canvas.itemconfig(self.lightGfx[player][side], fill="red")
        else:
            self.canvas.itemconfig(self.lightGfx[player][side], fill="")
            #if (self.lightGfx[player][side]):
            #    self.canvas.delete(self.lightGfx[player][side])

    def noteOn(self, midiNum):
        os.system("echo '0 " + str(midiNum) + " 120;' | pdsend 3001")

    def noteOff(self, midiNum):
        os.system("echo '0 " + str(midiNum) + " 0;' | pdsend 3001")

    def hipButtonPress(self, player = None, buttonIdx = None):

        fillColor = "n/a"
        if (player == 0):
            fillColor = "black"
        else:
            fillColor = "gray"
                
        self.canvas.itemconfig(self.hipButtonGfx[player], fill=fillColor)

    def hipButtonRelease(self, player = None, buttonIdx = None):
        self.canvas.itemconfig(self.hipButtonGfx[player], fill="")

    def triggerMisslapPenalty(self, player):
        pass
    
    def triggerPrematureSlapPenalty(self, playerIdx):
        pass
    
    def triggerLeaveHipPenalty(self, playerIdx):
        pass
    
    def slapPress(self, playerIdx, buttonIdx): #player = person getting slapped, button = button they slapped
        
        #outline box, for pc development
        self.canvas.itemconfig(self.lightGfx[playerIdx][buttonIdx], width = 5)

        if self.slapCallback != None:
            self.slapCallback(playerIdx, buttonIdx)
        '''
        if self.ticksUntilSlapCtr == self.ticksUntilSlap:
            #print "slap!"

            self.setLightOn(playerIdx, buttonIdx, False)

            self.triggerMisslapPenalty(self.getOpponentIdx(playerIdx))
            for j in range(2):
                self.setLightOn(playerIdx, j, False)
            
            self.ticksUntilSlap = random.randint(12, 50)
            self.ticksUntilSlapCtr = 0
            self.qtrNoteDuration = self.QNOTE_DELAY
            self.update()
        else:
            self.triggerPrematureSlapPenalty(self.getOpponentIdx(playerIdx))
        '''

    def slapRelease(self, playerIdx, buttonIdx):
        self.canvas.itemconfig(self.lightGfx[playerIdx][buttonIdx], width = 1)
    
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
        sys.exit(0)

    def keyPressed( self, event ):
        #event.char )
        
        #self.message1.set( "Key pressed: " + self.keysPressed[0])
        
        if not (event.char in self.keysPressed):
            #print "click " + event.char
            
            slapPlayerIndex=None
            slapButtonIndex=None
            hipButtonIndex = None
            
            for i in range(2):
                
                if event.char == SynthController.HIP_KEYS[i]:
                    self.hipButtonPress(i)
                
                for j in range(2):
                    if event.char == SynthController.SLAP_KEYS[i][j]:
                        self.slapPress(i, j)

            self.keysPressed.add(event.char)
    
        #self.message1.set( "Key pressed: " + event.char )

        if event.keysym == 'Escape':
            self.quit()
            self.quit()

        return "break"

    def keyReleased( self, event ):
        #self.synthCon.deslap()
        #print( "Key released: " + event.char )
        if (event.char in self.keysPressed):
            self.keysPressed.remove(event.char)
            for i in range(2):
                if event.char == SynthController.HIP_KEYS[i]:
                    self.hipButtonRelease(i)
                for j in range(2):
                    if event.char == SynthController.SLAP_KEYS[i][j]:
                        self.slapRelease(i, j)


if __name__ == "__main__":
    print "Go"
    synthCon = SynthController()
    synthCon.update()
    synthCon.mainloop()
    