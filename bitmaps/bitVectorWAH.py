import numpy as np



class bitVector:

    #######################################################################
    #                         Helper Functions                            #
    #######################################################################

    def getLen(self):
        # gets the length of the run word 
        return (self.storage[self.activeWordIndex] & ~(np.uint64(3) << np.uint64(62)))

    def moveIteratorForward(self,numWords):
        
        while(numWords > 0):
            # Because the length remaining does not include current word, then lenRemaining == 0 means that we are finished with the current run or literal.
            if self.lenRemaining == 0:
                self.activeWordIndex += 1
                # If new active word is a run, set length remaining accordingly. 
                if ( self.storage[self.activeWordIndex] >> np.uint64(63) ) == 1:
                    self.lenRemaining = self.storage[self.activeWordIndex] & ~( np.uint64(3) << np.uint64(62) )
                # If new active word is a literal, set length to one
                else:
                    self.lenRemaining = 1
            
            # You processed a word, so decrease the length remaining.
            self.lenRemaining -= 1
            numWords -= 1
            
    def rewind(self):
        #goes to the first word of the BV
        self.activeWordIndex = 0

    def printBitVector(self):
        for i in self.storage:
            print np.binary_repr(i, width = 64)

    def isLiteral(self, word):
        return word >> self.wordSizeInBits - np.uint64(1) == 0

    def setBitInActiveWord(self,pos,bit):
        if bit == 0:
            self.storage[self.activeWordIndex] &= ~(np.uint64(1)<<(np.uint64(self.wordSizeInBits - 2) - np.uint64(pos)))
        else:
            self.storage[self.activeWordIndex] |=  (np.uint64(1)<<(np.uint64(self.wordSizeInBits - 2) - np.uint64(pos)))
    
    # Make sure that lenInWords can fit in the current storage
    def ensureStorageFits(self, lenInWords):
        if self.storage.size < lenInWords:
            # TODO: In the future, this should do something a bit more efficient, like growing in blocks of size 1.5*current length or something like that.
            self.storage.resize(lenInWords)
    
                       
    def appendRun(self, runType, length):
        
        word = np.uint64(1) << np.uint64(63)
        word += np.uint64(runType) << np.uint64(62)
        word += length
        
        prevRunType = self.storage[self.activeWordIndex - 1] & (np.uint64(1) << np.uint64(62))
        
        if prevRunType == runType:
            #Checks if length is too big to add to current run
            while (self.storage[self.activeWordIndex - 1] & ~(np.uint64(3) << np.uint64(62))) <= 4611686018427387903:
                #Adds one to the length 
                self.storage[self.activeWordIndex - 1] += length
            #If run becomes too large it will create an new run in the next spot in storage
            self.ensureStorageFits(new.activeWordIndex + 1)
            newRun = np.uint64(1) << np.uint64(63)
            newRun += np.uint64(runType) << np.uint64(62)
            newRun += 1
            self.storage[self.activeWordIndex] = newRun
            
        else:
            self.ensureStorageFits(new.activeWordIndex + 1)        
            
            self.storage[new.activeWordIndex] = word
            
            self.activeWordIndex += 1
      
        
    def appendWord(self, word):
        #appends a word to a bitVector based on logical operations
        #Will also check if word is a run and send it to appendRun which will add it
    
        #Case 1: word is run
        if word == ~(np.uint64(1) << np.uint64(63)) or word == np.uint64(0):
            runType = (word >> np.uint64(62)) & np.uint64(1)
            getLength = np.uint64(1) << np.uint(63)
            getLength += np.uint64(1) << np.uint64(62)
            length = word & ~(getLength)
            
            self.appendRun(runType,length)
            
        #Case 2: word is literal
        else:
            #Checks if bitVector needs to be expanded
            self.ensureStorageFits(new.activeWordIndex + 1)
            #Sets word in correct spot in bitVector
            self.storage[self.activeWordIndex] += word
            #Iterates the index to the new spot
            self.activeWordIndex += 1


    #######################################################################
    #                           Methods                                   #
    #######################################################################
        
    def __init__(self):

        #Creates bitVector
        self.storage = np.zeros(1,dtype=uint64)
        #Sets wordSize
        self.wordSizeInBits = np.uint64(64)
        
        
        #rows in word
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

        self.lenRemaining = 0 # this will help to keep track of the runs
        
        self.appendWordIndex = 0 # Location of the last word in the bitvector. The append function will *only* work with this index.
    
    def append(self,bit):
        self.numRows += 1
        
                   
        #adds the bit to the literal in the last space            
        self.setBitInActiveWord(self.partialLiteralLength,bit)
        
        self.partialLiteralLength += 1
        
        # Done:
        # Grow the storage and move the active word if needed.
        if self.partialLiteralLength == (self.wordSizeInBits - 1):

            #check for merge back. Note that active word is always a literal.
            if self.storage[self.appendWordIndex] == 0 or ~(self.storage[self.appendWordIndex] | np.uint64(1) << np.uint64(self.wordSizeInBits - 1)) == 0:
                print 'Found a run. Checking if we need to merge this back into the previous word.'
                #Sets active word to fill of type bit and size one
                self.storage[self.appendWordIndex] = np.uint64(1)<<(np.uint64(self.wordSizeInBits - 1)) | (np.uint64(bit) << (np.uint64(self.wordSizeInBits - 2))) | np.uint64(1)
                
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
        
    def xor(self, other):

        #Checks if Bit Vectors are same size (throws error if not)
        if len(self.storage) != len(other.storage):
            print "Bit Vectors are not the same size. Error."
            break
        
        #Sets activeWordIndex to zero for both self and other
        self.activeWordIndex = 0
        other.activeWordIndex = 0

        #Creates new bitVector to hold xor operation
        new = bitVector()
        
        #FIXME: Not sure how to iterate this 
        for i in range(len(self.storage)):
            
            #checks for cases
            selfCheck = self.storage[self.activeWordIndex] >> np.uint64(63)
            otherCheck = other.storage[other.activeWordIndex] >> np.uint64(63)
            
            #Case 1: Both are literals
            if selfCheck == otherCheck and selfCheck == 0:
                newWrd = self.storage[self.activeWordIndex] ^ other.storage[other.activeWordIndex]
                newWrd &= ~(np.uint64(1) << np.uint64(63))
                new.appendWord(newWrd)
                
                self.moveIteratorForward(1)
                other.moveIteratorForward(1)
                
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
            
        
        self.storage = self.new

    def Or(self, other):
        
        new = bitVector()

        #Checks that vectors are the same size
        if self.numRows != other.numRows:
            print "Error: Vectors are of unequal size"
            return
        
        #sets activeWordIndex to zero for both self and other
        self.activeWordIndex = 0
        other.activeWordIndex = 0
        for i in range(len(self.storage)):
            
            #Determines whether the word is a literal or a run
            selfCheck = self.storage[self.activeWordIndex] >> np.uint64(63)
            otherCheck = other.storage[other.activeWordIndex] >> np.uint64(63)
            
            #Case 1: Both are literals
            if selfCheck == otherCheck and selfCheck == 0:
                newWrd = self.storage[self.activeWordIndex] | other.storage[other.activeWordIndex]
                newWrd &= ~(np.uint64(1) << np.uint64(63))
                
                new.appendWord(newWrd)
        
                self.activeWordIndex += 1
                other.activeWordIndex += 1
                
            #Case 2: Both are runs
            if selfCheck == otherCheck and otherCheck == 1:
                
                if self.getLen != other.getLen:
                    if self.getLen > other.getLen:
                        self.storage[self.activeWordIndex] -= other.getLen
                        totalLength = other.getLen
                    if other.getLen > self.getLen:
                        other.storage[other.activeWordIndex] -= self.getLen
                        totalLength = self.getLen
                else:
                    totalLength = self.getLen
                    
                #Determines whether run is of 1's or 0's
                selfRunType = (self.storage[self.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                otherRunType = (other.storage[other.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                    
                if selfRunType or otherRunType == 1:
                    self.appendRun(1, totalLength)
                if selfRunType and otherRunType == 0:
                    self.appendRun(0, totalLength)
                    
                    
                if self.getLen > other.getLen:
                    other.activeWordIndex += 1
                if self.getLen < other.getLen:
                    self.activeWordIndex += 1
                else: 
                    self.activeWordIndex += 1
                    other.activeWordIndex += 1
                
            
            #Case 3: One is a literal, one is a run
            if selfCheck != otherCheck:
                
                if selfCheck == 1 and otherCheck == 0:
                    #Determines whether run is of 1's or 0's
                    selfRunType = (self.storage[self.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                    
        print new
                
    def AND(self, other):
        # Make sure we are starting with the first word
        self.activeWordIndex = 0
        other.activeWordIndex = 0

        #create a new bit vector to store the result 
        new = bitVector()

        
        ##########
        # Fix Me #
        ##########

        for i in range(maxLen):

            # use bit shifting to see if we have fill words or literal words
            msbSelf = self.storage[self.activeWordIndex] & ( np.uint64(1) << np.uint64(63) )
            msbOther = other.storage[other.activeWordIndex] & ( np.uint64(1) << np.uint64(63) ) 

            #Case 1: if both are fill
            if msbSelf == 1 and msbOther == 1:
                #find what kind of fills we are dealing with
                selfRunType = self.storage[self.activeWordIndex] & ( np.uint64(1) << np.uint64(62) )
                otherRunType = other.storage[other.activeWordIndex] & ( np.uint64(1) << np.uint64(62) )

                #find the length of the fills
                selfLen = self.getLen()
                otherLen = other.getLen()

                #if both are fills of 0's iterate by the larger length
                if selfRunType == 0 and other == 0:
                    if selfLen > otherLen:
                        other.moveIteratorForward(selfLen)
                        new.appendWord( self.storage[self.activeWordIndex] )
                        self.activeWordIndex += 1

                    else:
                        self.moveIteratorForward(otherLen)
                        new.appendWord( other.storage[other.activeWordIndex] )
                        other.activeWordIndex += 1

                #if only self is a run of 0's
                elif selfRunType == 0:
                    other.moveIteratorForward(selfLen)                    
                    new.appendWord( self.storage[self.activeWordIndex] )
                    self.activeWordIndex += 1

                #if only other is a run of 0's
                elif otherRunType == 0:
                    self.moveIteratorForward(otherLen)
                    new.appendWord( other.storage[other.activeWordIndex] )
                    other.activeWordIndex += 1
                    
            #Case 2: if only self is a fill
            elif msbSelf == 1:

                #find if its a fill of 0's or 1's
                selfRunType = self.storage[self.activeWordIndex] & ( np.uint64(1) << np.uint64(62) )

                #find the length of the fill
                selfLen = self.getLen()

                #if the fill is of 0's than just write the fill
                if selfRunType == 0:
                    other.moveIteratorForward(selfLen)
                    new.appendWord( self.storage[self.activeWordIndex] )
                    self.activeWordIndex += 1

                #if the fill is of 1's than iterate through 
                else:
                    #creating variables that will help us later
                    otherRunType = 0
                    msbOther = 0

                    for i in range(selfLen):
                        #check to see if we incounter a fill of 0's, break if we do
                        if (otherRunType == 0 & msbOther == 1 ):
                            self.lenRemaining = selfLen - i
                            break
                        else:
                            #since anything '&' with 1 is itself we can just add the 'other' word
                            new.appendWord(other.storage[other.activeWordIndex])


                            other.moveIteratorForward(1)

                            #update to check for a fill of 0's
                            otherRunType = other.storage[other.activeWordIndex] & ( np.uint64(1) << np.uint64(62) )
                            msbOther = other.storage[other.activeWordIndex] & ( np.uint64(1) << np.uint64(63) ) 
                    

            
            #Case 3: if only other is a fill
            elif msbOther == 1:
                #find if its a fill of 0's or 1's
                otherRunType = other.storage[other.activeWordIndex] & ( np.uint64(1) << np.uint64(62) )
                                
                #find the length of the fill
                otherLen = other.getLen()

                if otherRunType == 0:
                    self.moveIteratorForward(otherLen)
