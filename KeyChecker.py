from Tkinter import *
from time import *
import threading

class KeyChecker(Frame):
    def __init__( self, keys):
        Frame.__init__( self )
        
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
        
        self.master.bind( "<KeyPress>", self.keyPressed )
        self.master.bind( "<KeyRelease>", self.keyReleased )
    
        self.keys = keys
        self.keysPressed = [True] * len(keys)
    
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
    
    def setLightOn(self, player, side, on):
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


    def hipButtonPress(self, player, buttonIdx, pressed):
    
        fillColor = ""
        if pressed:
            if (player == 0):
                fillColor = "black"
            else:
                fillColor = "gray"
    
        self.canvas.itemconfig(self.hipButtonGfx[player], fill=fillColor)


    def keyPressed( self, event ):
        for i in range(len(self.keys)):
            key = self.keys[i]
            if key == event.keysym:
                self.keysPressed[i] = False
                #print(event.char)
                self.message1.set( "Key pressed: " + event.char )
    
    def keyReleased( self, event ):
        for i in range(len(self.keys)):
            key = self.keys[i]
            if key == event.keysym:
                self.keysPressed[i] = True
                self.message1.set( "Key released: " + event.char )

    def buttonPressed(self, idx):
        return self.keysPressed[idx]
    
    def start(self):
        self.after(0)
        self.mainloop()