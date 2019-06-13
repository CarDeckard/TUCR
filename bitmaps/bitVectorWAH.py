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
        if self.partialLiteralLength == (self.wordSizeInBits - 1):

            #check for merge back. Note that active word is always a literal.
            if self.storage[self.activeWordIndex] == 0 or ~(self.storage[self.activeWordIndex] | np.uint64(1) << np.uint64(self.wordSizeInBits - 1)) == 0:
                print 'Found a run. Checking if we need to merge this back into the previous word.'
                #Sets active word to fill of type bit and size one
                self.storage[self.activeWordIndex] = np.uint64(1)<<(np.uint64(self.wordSizeInBits - 1)) | (np.uint64(bit) << (np.uint64(self.wordSizeInBits - 2))) | np.uint64(1)
                
                # Not done:
                #FIXME: need to check overflow for size of run
                
                # Do the merge if last word is the right type
                if self.activeWordIndex > 0 and self.storage[self.activeWordIndex - 1] >> np.uint64(62) == self.storage[self.activeWordIndex] >> np.uint64(62):
                    self.storage[self.activeWordIndex - 1] += np.uint64(1)
                    self.storage[self.activeWordIndex] = np.uint64(0)
                    self.partialLiteralLength = 0
                
                # Don't do the merge if the last word is the wrong type.
                else:
                    self.ensureStorageFits(self.numWords + 1)
                    self.partialLiteralLength = 0
                    self.activeWordIndex += 1
                    self.numWords += 1
                
            #Checks if not fill and needs to be expanded
            else:
                #print 'Hey booboo'
                self.ensureStorageFits(self.numWords + 1)
                self.partialLiteralLength = 0
                self.activeWordIndex += 1
                self.numWords += 1
                   
    def appendRun(self,runType,length):
        
        word = np.uint64(1) << np.uint64(63)
        word += np.uint64(runType) << np.uint64(62)
        word += length
        
        prevRunType = self.newBitVector[self.newBitVectorIndex - 1] & (np.uint64(1) << np.uint64(62))
        
        if prevRunType == runType:
            self.newBitVector[self.newBitVectorIndex - 1] += length
        else:
            self.ensureNewBitVectorFits(self.newBitVectorIndex + 1)        
            
            self.newBitVector[self.newBitVectorIndex] = word
            
            self.newBitVectorIndex += 1
      
    def appendWord(self,word):
        #appends a word to a new bitVector based on logical operations
        #Will also check if word is a run
    
        #Case 1: word is run
        if word == ~(np.uint64(1) << np.uint64(63)) or word == np.uint64(0):
            runType = (word >> np.uint64(62)) & np.uint64(1)
            getLength = np.uint64(1) << np.uint(63)
            getLength += np.uint64(1) << np.uint64(62)
            length = word & ~(getLength)
            
            self.appendRun(runType,length)
            
        #Case 2: word is literal
        else:
            #CHecks if newBitVector needs to be expanded
            self.ensureNewBitVectorFits(self.newBitVectorIndex + 1)
            #Sets word in correct spot in newBitVector
            self.newBitVector[self.newBitVectorIndex] += word
            #Iterates the index to the new spot
            self.newBitVectorIndex += 1
        
        
    def xor(self, other):
        
        #Sets activeWordIndex to zero for both self and other
        self.activeWordIndex = 0
        other.activeWordIndex = 0
        for i in range(len(self.storage)):
            
            #checks for cases
            selfCheck = self.storage[self.activeWordIndex] >> np.uint64(63)
            otherCheck = other.storage[other.activeWordIndex] >> np.uint64(63)
            
            #Case 1: Both are literals
            if selfCheck == otherCheck and selfCheck == 0:
                newWrd = self.storage[self.activeWordIndex] ^ other.storage[other.activeWordIndex]
                newWrd &= ~(np.uint64(1) << np.uint64(63))
                self.appendWord(newWrd)
                
                self.activeWordIndex += 1
                other.activeWordIndex += 1
                
            #Case 2: Both are fills
            if selfCheck == otherCheck and selfCheck == 1:
                
                getLength = np.uint64(1) << np.uint(63)
                getLength += np.uint64(1) << np.uint64(62)
                selfLength = self.storage[self.activeWordIndex] & ~(getLength)
                otherLength = other.storage[other.activeWordIndex] & ~(getLength)
                
                if selfLength != otherLength:
                    if selfLength > otherLength:
                        self.storage[self.activeWordIndex] -= otherLength
                        totalLength = otherLength
                    if otherLength > selfLength:
                        other.storage[other.activeWordIndex] -= selfLength
                        totalLength = selfLength
                else:
                    totalLength = selfLength
                        
                
                selfRunType = (self.storage[self.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                otherRunType = (other.storage[other.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                
                if selfRunType == otherRunType and selfRunType == 1:
                    self.appendRun(1,totalLength)
                if selfRunType == otherRunType and selfRunType == 0:
                    self.appendRun(0,totalLength)
                if selfRunType != otherRunType:
                    self.appendRun(1,totalLength)
                    
                if selfLength > otherLength:
                    other.activeWordIndex += 1
                if selfLength < otherLength:
                    self.activeWordIndex += 1
                else:
                    self.activeWordIndex += 1
                    other.activeWordIndex += 1

            #Case 3: One is literal and one is run
            if selfCheck != otherCheck and (selfCheck == 0 or otherCheck == 0):
                
                if selfCheck == 1:
                    selfRunType = (self.storage[self.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                    if selfRunType == 1:                    
                        tmpWrd = ~(np.uint64(1) << np.uint64(63))
                        tmpWrd += np.uint64(1) << np.uint64(63)
                    else:
                        tmpWrd = np.uint64(1) << np.uint64(63)
                    
                if otherCheck == 1:
                    otherRunType = (other.storage[other.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                    if otherRunType == 1:
                        tmpWrd = ~(np.uint64(1) << np.uint64(63))
                        tmpWrd += np.uint64(1) << np.uint64(63)
                    else:
                        tmpWrd = np.uint64(1) << np.uint64(63)
                        
                if selfCheck == 0:
                    newWrd = self.storage[self.activeWordIndex] ^ tmpWrd
                    newWrd &= ~(np.uint64(1) << np.uint64(63))
                    self.appendWord(newWrd)
                if otherCheck == 0:
                    newWrd = other.storage[other.activeWordIndex] ^ tmpWrd
                    newWrd &= ~(np.uint64(1) << np.uint64(63))
                    self.appendWord(newWrd)
                    
                if selfCheck == 1:
                    getLength = np.uint64(1) << np.uint(63)
                    getLength += np.uint64(1) << np.uint64(62)
                    selfLength = self.storage[self.activeWordIndex] & ~(getLength)
                    if selfLength - 1 == 0:
                        self.activeWordIndex += 1
                    else:
                        self.storage[self.activeWordIndex] -= 1
                    other.activeWordIndex += 1
                        
                if otherCheck == 1:
                    getLength = np.uint64(1) << np.uint(63)
                    getLength += np.uint64(1) << np.uint64(62)
                    otherLength = other.storage[other.activeWordIndex] & ~(getLength)
                    if otherLength - 1 == 0:
                        other.activeWordIndex += 1
                    else:
                        other.storage[other.activeWordIndex] -= 1
                    self.activeWordIndex += 1
            
        
        self.storage = self.newBitVector

    def AND(self, other):
        self.activeWordIndex = np.uint64(0)
        other.activeWordIndex = np.uint64(0)

        
        if len(other.storage) > len(self.storage):
            maxlen = len(other.storage)
        else:
            maxlen = len(self.storage)
        
        for i in range(maxlen):
            
            #find the most significant bit to see if Fill or Literal
            msbSelf = self.storage[self.activeWordIndex] >> np.uint64(63)
            msbOther = other.storage[other.activeWordIndex] >> np.uint64(63)
            
            #If either are fill words enter here
            if msbSelf == 1 or msbOther == 1:
                
                #If both are Fill Words
                if msbSelf == 1 and msbOther == 1:
                    
                    #Use a mask to find if we have a run of 1's or 0's
                    #If nonzero we have a run of 1's
                    runSelf = self.storage[self.activeWordIndex] & np.uint64(4611686018427387904)
                    runOther = other.storage[other.activeWordIndex] & np.uint64(4611686018427387904)
                
                    #Use a mask to find the length of our runs
                    lenSelf = self.storage[self.activeWordIndex] & np.uint64(4611686018427387903)
                    lenOther = other.storage[other.activeWordIndex] & np.uint64(4611686018427387903)
                    
                    #If they are both runs of 1's set NewBitVector to a run of 1's
                    if runSelf != 0 and runOther != 0:
                        self.appendWord(np.uint64(13835058055282163713))
                    #If one of them is 0's then set NewBitVector to run of 0's
                    else:
                        self.appendWord(np.uint64(9223372036854775809))
                        
                        
                    #Iterate the active word index only if the run is done
                    if lenSelf == 1:
                        self.activeWordIndex += 1
                    else:
                        self.storage[self.activeWordIndex] -= np.uint64(1)
                    if lenOther == 1:
                        other.activeWordIndex += 1
                    else:
                        other.storage[other.activeWordIndex] -= np.uint64(1)
                        
                    
                #If Self is a Fill word and Other is a Literal
                elif msbSelf == 1:
                    
                    #Use a mask to find if we have a run of 1's or 0's
                    #If nonzero we have a run of 1's
                    runSelf = self.storage[self.activeWordIndex] & np.uint64(4611686018427387904)
                
                    #Use a mask to find the length of our runs
                    lenSelf = self.storage[self.activeWordIndex] & np.uint64(4611686018427387903)
                    
                    if runSelf == 1:
                        
                        #if we have a run of 1's than just append other to NewBitVector
                        self.appendWord(other.storage[other.activeWordIndex])
                        
                    else:
                        
                        #if we have a run of 0's than just append 0's to NewBitVector
                        self.appendWord(0)
                        
                    #Iterate Self Index if run is finished
                    if lenSelf == 1:
                        self.activeWordIndex += 1
                    else:
                        self.storage[self.activeWordIndex] -= np.uint64(1)
                        
                    other.activeWordIndex += 1
                        
                #If Other is a Fill word and Self is a Literal
                else:
                    #Use a mask to find if we have a run of 1's or 0's
                    #If nonzero we have a run of 1's
                    runOther = other.storage[other.activeWordIndex] & np.uint64(4611686018427387904)
                
                    #Use a mask to find the length of our runs
                    lenOther = other.storage[other.activeWordIndex] & np.uint64(4611686018427387903)
                    
                    if runOther == 1:
                        
                        #if we have a run of 1's than just append other to NewBitVector
                        self.appendWord(self.storage[self.activeWordIndex])
                        
                    else:
                        
                        #if we have a run of 0's than just append 0's to NewBitVector
                        self.appendWord(0)
                        
                    #Iterate Self Index if run is finished
                    if (lenOther - 1) == 0:
                        other.activeWordIndex += 1
                    else:
                        other.storage[other.activeWordIndex] -= np.uint64(1)
                        
                    self.activeWordIndex += 1
                
            #If both are Literal enter here
            else:
                newBV = self.storage[self.activeWordIndex] & other.storage[other.activeWordIndex]
                self.appendWord(np.uint64(newBV))
                
                #Iterate the Index values
                self.activeWordIndex += 1
                other.activeWordIndex += 1
        
        #rewrite storage as the new vector of self AND other
        self.storage = self.NewBitVector


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
    

c = bitVector()
d = bitVector()
