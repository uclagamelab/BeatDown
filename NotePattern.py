import random

class NotePattern:

    REST = -1
    NOTE_SEQS = [\
                 [60, 60, 67, 67, 69, 69, 67, REST],
                 [60, 64, 67, 72, 67, 64],
                 [60,72,60,72,60,72,59,71],
                   [60, REST, 55, REST, 60, REST, 55, REST, 60,  REST, 55, REST, 60, 55,  57, 59],
                [60, 62, 64, 65, 67, 69, 71, 72, 71, 69, 67, 65, 64, 62, 60],
                ]
    
    #[60, 60, 60, REST, 72, 71, 72, REST],
    #[60, 59, 57, 55, 57, 59]
                    #[60, 64, 67, 72, 67, 64]\
                    #[60, 62, 64, 66, 68, 70, 72, 70, 68, 66, 64, 62],\
                        #[60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 61],\
                        #[60, 64, 66, 67, 72, 67, 66, 64]\
    
    def __init__(self):
        self.currentSeqIndex = 0
        self.noteIdx = -1 # start on last note, to make loop easier
        self.notes = NotePattern.NOTE_SEQS[0]
        self.transpose = 0
        self.transposeOk = False

    def randomlyTranspose(self):
        transpos = [1, 2, 5, 7]
        probs    = [.3, .3, .3, .1]

        acc = 0
        diceSz = 100
        roll = random.random()
        jump = 0
        for i in range(len(probs)):
            if roll > probs[i] + acc:
                acc = acc + probs[i]
            else:
                jump = transpos[i]
    
        jump = jump * (2*random.randint(0,1)) - 1 # +/- 1
        #self.transpose = self.transpose + (2*random.randint(0,1)) - 1 # just transpose a random half step
        if (self.transpose + jump < -12 and jump < 0) or (self.transpose + jump > 12 and jump > 0):
            jump = -jump
       
        self.transpose = self.transpose + jump
    
    def tick(self):
        
        #demand that a whole sequence finishes before a transpose
        if ( self.noteIdx == len(self.notes) - 1 ):
            self.transposeOk = True
        
        self.noteIdx = (self.noteIdx + 1) % len(self.notes)
        
        if self.noteIdx == 1 and self.transposeOk: #just played 1st note (root), can change key
            # 1 / 3 change of key change
            if random.randint(1,2) == 2:
                self.randomlyTranspose()
                self.noteIdx = 0
                self.transposeOk = False
                
        
        if self.noteIdx == 0: # last note of sequence, maybe switch sequence
            changeSequenceRoll = random.randint(0,1)
            if changeSequenceRoll == 1:
                newSeq = random.randint(0, len(NotePattern.NOTE_SEQS) - 1)

                # but don't repeat!
                if newSeq == self.currentSeqIndex:
                    newSeq = (newSeq + 1) % len(NotePattern.NOTE_SEQS)
                self.notes = NotePattern.NOTE_SEQS[newSeq]
                self.currentSeqIndex = newSeq

    
    def getCurrentNote(self):
        if self.notes[self.noteIdx] != NotePattern.REST:
            return self.notes[self.noteIdx] + self.transpose
        else:
            return NotePattern.REST
