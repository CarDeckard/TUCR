import numpy as np



class bitVector:
   
        
    
    def __init__(self):

        #Make empty array of proper size
        self.storage = np.zeros(1,dtype=np.uint64)
        #Prints to check if correct
        print self.storage        
        self.wordSizeInBits = np.uint64(64)
        #Sets number of rows in word
        self.numRows = 0

        # This implementation is designed so that the partial literal length is always < wordSizeInBits - 1.
        # See also comments on activeWordIndex.
        #length of last literal
        self.partialLiteralLength = 0
        #Sets numWords to zero
        self.numWords = 1 # length of storage
        
        # Important: This implementation is designed such that the active word is always a literal.
        # Another literal is always added if the active word gets full.
        self.activeWordIndex = 0 # this is the index of the active word
        
        #New Vector Storage Variables
        self.newBitVector = np.zeros(1,dtype=np.uint64)
        
        self.newBitVectorIndex = 0
        
        self.numNewWords = 0
        
    
    def isLiteral(self,word):
        return word >> self.wordSizeInBits - np.uint64(1) == 0

    def setBitInActiveWord(self,pos,bit):
        if bit == 0:
            self.storage[self.activeWordIndex] &= ~(np.uint64(1)<<(np.uint64(self.wordSizeInBits - 2) - np.uint64(pos)))
        else:
            self.storage[self.activeWordIndex] |=  (np.uint64(1)<<(np.uint64(self.wordSizeInBits - 2) - np.uint64(pos)))
    
    # Make sure that newLenInWords can fit in the current storage
    def ensureStorageFits(self,newLenInWords):
        if self.storage.size < newLenInWords:
            # TODO: In the future, this should do something a bit more efficient, like growing in blocks of size 1.5*current length or something like that.
            self.storage.resize(newLenInWords)
    def ensureNewBitVectorFits(self,newLenInWords):    
        if self.newBitVector.size < newLenInWords:
            self.newBitVector.resize(newLenInWords)
    
    def append(self,bit):
        self.numRows += 1
        
                   
        #adds the bit to the literal in the last space            
        self.setBitInActiveWord(self.partialLiteralLength,bit)
        
        self.partialLiteralLength += 1
        
        # Done:
        # Grow the storage and move the active word if needed.
        if self.partialLiteralLength == self.wordSizeInBits - 1:
            print 'Checking if we need to merge this back into the previous word.' 

            #check for merge back
            if self.storage[self.activeWordIndex] == 0 or ~(self.storage[self.activeWordIndex] | np.uint64(1) << np.uint64(self.wordSizeInBits - 1)) == 0:
                #Sets active word to fill of type bit and size one
                self.storage[self.activeWordIndex] = np.uint64(1)<<(np.uint64(self.wordSizeInBits - 1)) | (np.uint64(bit) << (np.uint64(self.wordSizeInBits - 2))) | np.uint64(1)
                # Not done:
                #FIXME: need to check overflow
                if self.activeWordIndex > 0 and self.storage[self.activeWordIndex - 1] >> np.uint64(62) == self.storage[self.activeWordIndex] >> np.uint64(62):
                    self.storage[self.activeWordIndex - 1] += np.uint64(1)
                    self.storage[self.activeWordIndex] = np.uint64(0)
                    self.partialLiteralLength = 0
                else:
                    self.ensureStorageFits(self.numWords + 1)
                    self.partialLiteralLength = 0
                    self.activeWordIndex += 1
                    self.numWords += 1
            #Checks if not fill and needs to be expanded    
            if self.storage[self.activeWordIndex - 1] >> np.uint64(63) == 0b0:
                print 'Hey booboo'
                self.ensureStorageFits(self.numWords + 1)
                self.partialLiteralLength = 0
                self.activeWordIndex += 1
                self.numWords += 1
                   
    def appendRun(self,runType,length):
        
        word = np.uint64(1) << np.uint64(63)
        word += np.uint64(runType) << np.uint64(62)
        word += length
        
        self.newBitVector[self.newBitVectorIndex] = word
        
        self.ensureNewBitVectorFits(self.newBitVectorIndex + 1)
        
        self.newBitVectorIndex += 1
      
    def appendWord(self,word):
        #appends a word to a new bitVector based on logical operations
        #Will also check if word is a run
    
        #Case 1: word is literal
        if word >> np.uint64(63) == 0:
            #Sets word in correct spot in newBitVector
            self.newBitVector[self.newBitVectorIndex] = word
            #CHecks if newBitVector needs to be expanded
            self.ensureNewBitVectorFits(self.newBitVectorIndex + 1)
            #Iterates the index to the new spot
            self.newBitVectorIndex += 1
        #Case 2: word is run
        else:
            runType = (word >> np.uint64(62)) & np.uint64(1)
            getLength = np.uint64(1) << np.uint(63)
            getLength += np.uint64(1) << np.uint64(62)
            length = word & ~(getLength)
            
            self.appendRun(runType,length)
        
    def xor(self, other):
        
        #Sets activeWordIndex to zero for both self and other
        self.activeWordIndex = 0
        other.activeWordIndex = 0
        for i in range(len(other.storage)):
            
            #checks for cases
            selfCheck = self.storage[self.activeWordIndex] >> np.uint64(63)
            otherCheck = other.storage[other.activeWordIndex] >> np.uint64(63)
            
            #Case 1: Both are literals
            if selfCheck == otherCheck and selfCheck == 0:
                newWrd = self.storage[self.activeWordIndex] ^ other.storage[other.activeWordIndex]
                self.appendWord(newWrd)
                #FIXME: ensureFits needs to be fixed to account for newBitVector
                #Checks if storage needs expanded
                self.ensureNewBitVectorFits(self.numNewWords + 1)
        
            self.activeWordIndex += 1
            other.activeWordIndex += 1
            print self.newBitVector
        
    def Or(self, other):
        
        #sets activeWordIndex to zero for both self and other
        self.activeWordIndex = 0
        other.activeWordIndex = 0
        for i in range(len(other.storage)):
            
            #Determines whether the word is a literal or a run
            selfCheck = self.storage[self.activeWordIndex] >> np.uint64(63)
            otherCheck = other.storage[other.activeWordIndex] >> np.uint64(63)
            
            #Case 1: Both are literals
            if selfCheck == otherCheck and selfCheck == 0:
                newWrd = self.storage[self.activeWordIndex] | other.storage[other.activeWordIndex]
                self.appendWord(newWrd)
                self.ensureNewBitVectorFits(self.numNewWords + 1)
                
            #Case 2: One is a literal, one is a run
            if selfCheck != otherCheck:
                #Gets word count for
                if selfCheck == 1:
                    runCountBitVector = bitVector()
                    runCountBitVector.append(0)
                    runCountBitVector.append(0)
                    for n in range(62):
                        runCountBitVector.append(1)
                    
            #Case 3: Both are runs
            if selfCheck == otherCheck and otherCheck == 1:
                newWrd = self.storage[self.activeWordIndex] | other.storage[other.activeWordIndex]
                self.appendWord(newWrd)
                self.ensureNewBitVectorFits(self.newWords + 1)
            
            #Increment activeWordIndex and print the OR'ed word
            self.activeWordIndex += 1
            other.activeWordIndex += 1
            print self.newWrd
            
    def printBitVector(self):
        for i in self.storage:
            print np.binary_repr(i, width = 64)
    
data = np.array([4,5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4])
dataHeaders = np.unique(data)
c = bitVector()
#print dataHeaders
#for i in data:
#    if i == 4:
#        c.append(1)
#    else:
#        c.append(0)

c.printBitVector()

print c.numRows
