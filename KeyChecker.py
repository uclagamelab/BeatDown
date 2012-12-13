from Tkinter import *
from time import *
from InputChecker import *

class KeyChecker(Frame, InputChecker):
    def __init__( self, slapKeys, hipKeys, lightPins):
        Frame.__init__( self )
        
        
        self.slapKeys = slapKeys
        self.hipKeys = hipKeys
        self.lightPins = lightPins
        
        keys = []

        for playerKeys in slapKeys:
            keys.append(playerKeys[0])
            keys.append(playerKeys[1])

        keys.append(hipKeys[0])
        keys.append(hipKeys[1])
        
        InputChecker.__init__(self, keys, [])
    
        self.keysPressed = dict()
        for key in keys:
            self.keysPressed[key] = True
                
        
        
                
        def pressCb(key): self.graphicsCallback(key, True)
        def releaseCb(key): self.graphicsCallback(key, False)
        self.addPressCallback(pressCb)
        self.addReleaseCallback(releaseCb)
        
        self.pack( expand = YES, fill = BOTH )
        self.master.title( "BeatDown Debug" )
        self.master.geometry( "640x480" )
        
        self.message1 = StringVar()
        self.line1 = Label( self, textvariable = self.message1 )
        self.message1.set( "Type any key or shift" )
        self.line1.pack()
        
        self.message2 = StringVar()
        self.line2 = Label( self, textvariable = self.message2 )
        self.message2.set( "" )
        self.line2.pack()
        
        self.master.bind( "<KeyPress>", self.keyPressed_cb )
        self.master.bind( "<KeyRelease>", self.keyReleased_cb )
    
    
        self.canvas = Canvas(self, width=640, height=480)
        self.canvas.pack()
        
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

    # for graphics purposes
    
    def graphicsCallback(self, key, pressed):
        slapPlayerSide = self.getSlapKeyPlayerSidePair(key)
        hipPlayer = self.getHipKeyPlayer(key)

        if slapPlayerSide != None:
            self.slapPress(slapPlayerSide[0], slapPlayerSide[1], pressed)

        if hipPlayer != None:
            self.hipButtonPress(hipPlayer, pressed)
        
    def getLightPinPlayerSidePair(self, pin):
        for p in range(len(self.lightPins)):
            for s in range(len(self.lightPins[p])):
                if self.lightPins[p][s] == pin:
                    return [p, s]
        return None

    def getSlapKeyPlayerSidePair(self, key):
        for p in range(len(self.slapKeys)):
            for s in range(len(self.slapKeys[p])):
                if self.slapKeys[p][s] == key:
                    return [p, s]
        return None
    
    def getHipKeyPlayer(self, key):
        for p in range(len(self.hipKeys)):
            if self.hipKeys[p] == key:
                return p
        return None
            
    def setLightOn(self, pin, on):
        pair = self.getLightPinPlayerSidePair(pin)

        player = pair[0]
        side = pair[1]
        
        if (on):
            self.canvas.itemconfig(self.lightGfx[player][side], fill="red")
        else:
            self.canvas.itemconfig(self.lightGfx[player][side], fill="")

    
    def slapPress(self, playerIdx, buttonIdx, pressed): #player = person getting slapped, button = button they slapped
        #outline box, for pc development
        lWidth = 1
        if pressed:
            lWidth = 5
        self.canvas.itemconfig(self.lightGfx[playerIdx][buttonIdx], width = lWidth)


    def hipButtonPress(self, player, pressed):
        fillColor = ""
        if pressed:
            if (player == 0):
                fillColor = "black"
            else:
                fillColor = "gray"
    
        self.canvas.itemconfig(self.hipButtonGfx[player], fill=fillColor)


    def keyPressed_cb( self, event ):
        self.keysPressed[event.keysym] = False
        self.message1.set( "Key pressed: " + event.keysym )

        if event.keysym == 'Escape':
            print "tkinter quit"
            self.quit()
            self.quitNow = True
    
    def keyReleased_cb( self, event ):
        self.keysPressed[event.keysym] = True
        self.message1.set( "Key released: " + event.keysym )
    
    def buttonPressed(self, idx):
        return self.keysPressed[idx]
    
    def start(self):
        self.mainloop()