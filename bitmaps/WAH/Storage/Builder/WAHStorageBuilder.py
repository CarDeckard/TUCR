# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 10:47:49 2019

@author: josiah_mcclurg
"""

class WAHStorageBitBuilder:
    ## @var numWords
    #  Length of the storage
    
    ## @var storage
    #  Stores the compressed bitmap
    
    ## @var numRows
    #  Length in bits of the uncompressed bitmap

    ## @var totalLength
    #  Length in words of the uncompressed bitmap

    ## @var appendWordIndex
    #  Index of the word onto which append will add a row. This is guaranteed
    #  to point to the last valid word in the compressed index. This word is
    #  guaranteed to be a literal.
    
    ## @var partialLiteralLength
    #  This implementation is designed so that the partial literal length is
    #  always < wordSizeInBits - 1.
    
    def __init__(self):
        self.numWords = 1       
        self.storage = np.zeros(1,dtype = np.uint64)        
        self.numRows = 0
        
        self.partialLiteralLength = 0
        self.appendWordIndex = 0
        self.totalLength = 0
    
    def setBitInAppendWord(self,pos,bit):
        """Sets a bit in the active word."""
        if bit == 0:
            self.storage[self.appendWordIndex] &= ~(np.uint64(1)<<(np.uint64(bitVectorWAH.wordSizeInBits - 2) - np.uint64(pos)))
        else:
            self.storage[self.appendWordIndex] |=  (np.uint64(1)<<(np.uint64(bitVectorWAH.wordSizeInBits - 2) - np.uint64(pos)))
    
    def ensureStorageFits(self, lenInWords):
        """Make sure that lenInWords can fit in the current storage"""
        
        if self.storage.size < lenInWords:
            # TODO: In the future, this should do something a bit more efficient, like growing in blocks of size 1.5*current length or something like that.
            self.storage.resize(lenInWords)  
            
    def appendWord(self, word):
        """appends a word to a bitVector based on logical operations
        
        Will also check if word is a run and send it to appendRun which will add it
        """
    
        #Case 1: word is run
        if word == ~(np.uint64(1) << np.uint64(63)) or word == np.uint64(0):
            runType = (word >> np.uint64(62)) & np.uint64(1)
            getLength = np.uint64(1) << np.uint64(63)
            getLength += np.uint64(1) << np.uint64(62)
            length = word & ~(getLength)
            
            self.appendRun(runType,length)
            
        #Case 2: word is literal
        else:
            #Checks if bitVector needs to be expanded
            self.ensureStorageFits(self.activeWordIndex + 1)
            #Sets word in correct spot in bitVector
            self.storage[self.activeWordIndex] += word
            #Iterates the index to the new spot
            self.activeWordIndex += 1

    def appendRun(self, runType, length):
    
        word = np.uint64(1) << np.uint64(63)
        word += np.uint64(runType) << np.uint64(62)
        word += length
        
        prevRunType = self.storage[self.activeWordIndex - 1] & (np.uint64(1) << np.uint64(62))
        
        if prevRunType == runType:
            #if we do not overrun by adding the length than just add the length
            # 4611686018427387903 is the max length that our fill words can represent
            if (self.getLen + length) < 4611686018427387903:
                self.storage[self.activeWordIndex - 1] += length
            
            #If run becomes too large it will create an new run in the next spot in storage                
            else:
                self.ensureStorageFits(self.activeWordIndex + 1)
                newRun = np.uint64(1) << np.uint64(63)
                newRun += np.uint64(runType) << np.uint64(62)
                newRun += 1
                self.storage[self.activeWordIndex] = newRun
            
        else:
            self.ensureStorageFits(self.activeWordIndex + 1)        
            
            self.storage[self.activeWordIndex] = word
            
            self.activeWordIndex += 1
    
    def append(self,bit):
        self.numRows += 1
        
                   
        #adds the bit to the literal in the last space            
        self.setBitInAppendWord(self.partialLiteralLength,bit)
        
        self.partialLiteralLength += 1
        
        # Done:
        # Grow the storage and move the active word if needed.
        if self.partialLiteralLength == (bitVectorWAH.wordSizeInBits - 1):

            #check for merge back. Note that active word is always a literal.
            if self.storage[self.appendWordIndex] == 0 or ~(self.storage[self.appendWordIndex] | np.uint64(1) << np.uint64(bitVectorWAH.wordSizeInBits - 1)) == 0:
                print 'Found a run. Checking if we need to merge this back into the previous word.'
                #Sets active word to fill of type bit and size one
                self.storage[self.appendWordIndex] = np.uint64(1)<<(np.uint64(bitVectorWAH.wordSizeInBits - 1)) | (np.uint64(bit) << (np.uint64(bitVectorWAH.wordSizeInBits - 2))) | np.uint64(1)
                
                # Not done:
                #FIXME: need to check overflow for size of run
                
                # Do the merge if last word is the right type
                if self.appendWordIndex > 0 and self.storage[self.appendWordIndex - 1] >> np.uint64(62) == self.storage[self.appendWordIndex] >> np.uint64(62):
                    self.storage[self.appendWordIndex - 1] += np.uint64(1)
                    self.storage[self.appendWordIndex] = np.uint64(0)
                    self.partialLiteralLength = 0
                
                # Don't do the merge if the last word is the wrong type.
                else:
                    self.ensureStorageFits(self.numWords + 1)
                    self.partialLiteralLength = 0
                    self.appendWordIndex += 1
                    self.numWords += 1
                
            #Checks if not fill and needs to be expanded
            else:
                #print 'Hey booboo'
                self.ensureStorageFits(self.numWords + 1)
                self.partialLiteralLength = 0
                self.appendWordIndex += 1
                self.numWords += 1