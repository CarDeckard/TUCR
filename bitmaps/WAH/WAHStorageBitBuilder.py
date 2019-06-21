# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 10:47:49 2019

@author: josiah_mcclurg
"""
import numpy as np
from WAHStorageWordBuilder import WAHStorageWordBuilder

class WAHStorageBitBuilder(WAHStorageWordBuilder):    
    
    def __init__(self, initialSize = 1, wordSizeInBits = 64):
        # Initialize the storage
        super(WAHStorageBitBuilder, self).__init__(initialSize,wordSizeInBits)

        # Number of bits in the uncompressed bitmap
        self.numRows = 0
        
        # This implementation is designed so that the partial literal length is
        # always < wordSizeInBits - 1.
        self.partialLiteralLength = 0
    
    ## Sets a bit in the active word.
    def setBitInAppendWord(self,pos,bit):
        pos = self.dtype(pos)
        if bit == 0:
            self.storage[self.appendWordIndex] &= ~(self.dtype(1) << (self.runSizeInBits - pos))
        else:
            self.storage[self.appendWordIndex] |=  (self.dtype(1) << (self.runSizeInBits - pos))
    
    def appendWord(self,word):
        if self.partialLiteralLength == 0:
            super(WAHStorageBitBuilder,self).appendWord(word)
        else:
            raise Exception("Cannot append a word right now. Make you have filled out the current one first.")
    
    def appendRun(self,runType,length):
        if self.partialLiteralLength == 0:
            super(WAHStorageBitBuilder,self).appendRun(runType,length)
        else:
            raise Exception("Cannot append a word right now. Make you have filled out the current one first.")
    
    ## Not to be confused with appendRun, appendBits appends the specified number of bits
    #  FIXME: This can be implemented much more efficiently using a combination of appendRun
    #  and appropriate bit masks. Right now, it just uses append in a loop.
    def appendBits(self, runType, numBits):
        for i in range(numBits):
            self.append(runType)
        
    ## Appends individual bits to the vector
    def append(self,bit):
        self.numRows += 1
                   
        #adds the bit to the literal in the last space            
        self.setBitInAppendWord(self.partialLiteralLength, bit)
        
        self.partialLiteralLength += 1
        
        # Done:
        # Grow the storage and move the active word if needed.
        if self.partialLiteralLength == self.literalSizeInBits:
            
            # Since appendWordIndex points to the location at which the literal will be inserted,
            # the following line is correct.
            self.partialLiteralLength = 0
            self.appendWord(self.storage[self.appendWordIndex])
    
    ## Represents the compressed bit vector in binary format, marking where the words end.
    def __str__(self):
        s = ""
        for i in range(self.storage.size):
            s += np.binary_repr(self.storage[i], width = self.wordSizeInBits)+"\n"
            if i == self.appendWordIndex:
                s += "-" * int(1 + self.partialLiteralLength)
                s += "|"
                s += "-" * int(self.wordSizeInBits - (2 + self.partialLiteralLength))
                s += "\n"
            
        return s
if __name__ == "__main__":
    print "Running some testing code..."
    a = WAHStorageBitBuilder()
    a.appendBits(1,60)
    a.appendBits(0,2)
    a.appendBits(0,1)
    a.appendRun(0,3)
    a.appendWord(0)
    print a
    a.appendWord((a.dtype(1) << a.literalSizeInBits) - a.dtype(1))
    print a