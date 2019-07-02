# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 10:47:49 2019

@author: josiah_mcclurg
"""

import numpy as np
from WAHStorage import WAHStorage

## This class allows you to build up a storage array one word at a time
class WAHStorageWordBuilder(WAHStorage):

    def __init__(self, initialSize = 1, wordSizeInBits = 64):
        # Initialize the storage
        super(WAHStorageWordBuilder, self).__init__(initialSize,wordSizeInBits)
        
    ## Make sure that lenInWords can fit in the current storage
    #  @param lenInWords - The compressed size (in words) that is supposed
    #  to fit inside storage. Resizes storage to fit if necessary.
    def ensureStorageFits(self, lenInWords):
        if self.storage.size < lenInWords:
            # TODO: In the future, this should do something a bit more efficient,
            # like growing in blocks of size 1.5*current length or something like that.
            self.storage.resize(lenInWords)  
           
    ## appends a word to a bitVector based on logical operations  
    #  Will also check if word is a run and send it to appendRun which will add it
    #
    def appendWord(self, word):
        word = self.dtype(word)
        if not self.isLiteral(word):
            raise Exception("word %s is not a literal"%(np.binary_repr(word, width=self.wordSizeInBits)))
            
        # The word is actually a run of type 0
        if word == self.dtype(0):
            self.appendRun(0,1)
        
        # The word is actually a run of type 1
        elif self.isLiteralRunOfOnes(word & ~(self.dtype(1) << self.literalSizeInBits)):
            self.appendRun(1,1)
        
        # The word is really is a literal
        else:
            #Sets word in correct spot in bitVector
            self.storage[self.appendWordIndex] = word
            
            #Iterates the index to the new spot
            self.appendWordIndex += 1
            
            #Checks if bitVector needs to be expanded
            self.ensureStorageFits(self.appendWordIndex+1)
        
            # Update the total number of words being represented
            self.totalLength += 1
            
    ## appends a run to the bitvector
    def appendRun(self, runType, length):
        runType = self.dtype(runType)
        length = self.dtype(length)
        
        # If the storage is NOT currently empty,
        # AND the word before the append literal location is a run
        # AND that run is of the appropriate type, then update that run length.
        # FIXME: also need to check that adding length to the run will not cause
        #        an overflow
        # In this special case, we can update the existing run.
        if (self.appendWordIndex > 0) and (not self.isLiteral(self.storage[self.appendWordIndex - 1])) and self.getRunType(self.storage[self.appendWordIndex - 1]) == runType:
            print "merging"
            self.storage[self.appendWordIndex - 1] += length

        # We must append a new run
        else:
            print "appending new"
            self.storage[self.appendWordIndex] = ((self.dtype(2) | runType) << self.runSizeInBits) | length
            
            self.appendWordIndex += 1
            self.ensureStorageFits(self.appendWordIndex+1)
        
        # Update the total number of words being represented
        self.totalLength += length