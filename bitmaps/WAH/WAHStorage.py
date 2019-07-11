# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 13:25:30 2019

@author: josiah_mcclurg
"""

import numpy as np

## This class is responsible for containing a compressed bitmap.
#  It also allows you to interact with the compressed bitmap
#  at a very basic level.
class WAHStorage(object):
    
    ## Initialize the storage
    #  @param initialSize - initial size of the storage array
    #  @param wordSizeInBits - word size of the storage array
    def __init__(self, initialSize = 1, wordSizeInBits = 64):
        # Makes sure the data type is correct for the specified word size
        if wordSizeInBits > 64:
            raise Exception("Word size cannot be bigger than 64.")
        elif wordSizeInBits > 32:
            self.dtype = np.int64
        elif wordSizeInBits > 16:
            self.dtype = np.int32
        elif wordSizeInBits > 8:
            self.dtype = np.int16
        else:
            self.dtype = np.int8
        
        # WAH-encoded literal: wordSizeInBits-bit word
        # [1-bit type header = 0] [literalSizeInBits-bit literal word]
        # 
        # WAH-encoded run: wordSizeInBits-bit word
        # [1-bit type header = 1] [1-bit run type] [runSizeInBits-bit run length
        # (specifies number of literalSizeInBits-bit words that this run represents)]
        self.wordSizeInBits = self.dtype(wordSizeInBits)
        self.literalSizeInBits = self.wordSizeInBits - self.dtype(1)
        self.runSizeInBits = self.wordSizeInBits - self.dtype(2)

        # Stores the compressed bitmap
        self.storage = np.zeros(initialSize,dtype = self.dtype)
        
        # Length in words of the uncompressed bitmap
        self.totalLength = 0
        
        # Index of the literal where the NEXT call to appendWord will go (assuming that it is indeed a literal)
        self.appendWordIndex = 0
    
    ## Assuming that the word is a literal, tells whether it is a run of ones
    def isLiteralRunOfOnes(self, word):
        return ~(word | (self.dtype(1) << self.literalSizeInBits)) == self.dtype(0)
    
    ## Tells whether the specified word is a literal or not.
    def isLiteral(self,word):
        return word >> self.literalSizeInBits == self.dtype(0)
    
    # Assuming that word is a run, gets the run type
    def getRunType(self,word):
        return (word >> self.runSizeInBits) & self.dtype(1)
    
    ## Assuming that word is a run, gets the run length.
    def getRunLen(self,word):
        # gets the length of the run word 
        return (word & ~(self.dtype(3) << self.runSizeInBits))
    
    ## Gets the number of words in the uncompressed version of this bitmap
    def getUncompressedLenInWords(self):
        return self.totalLength
    
    ## Returns the number of words alllocated for the bitmap.
    def getStorageSizeInWords(self):
        return self.storage.size
    
    ## Returns the number of words in the uncompressed bitmap
    def getTotalLength(self):
        return self.totalLength
    
    ## Returns the compressed word at the specified index
    def getWordAt(self, index):
        return self.storage[index]
    
    ## Represents the compressed bit vector in binary format, marking where the words end.
    def __str__(self):
        s = ""
        for i in range(self.storage.size):
            if i == self.appendWordIndex:
                s += "-" * self.wordSizeInBits + "\n"
            s += np.binary_repr(self.storage[i], width = self.wordSizeInBits)+"\n"
            
        return s