import numpy as np

class bitVector:

    #######################################################################
    #                         Helper Functions                            #
    #######################################################################

    def getFirstLenRemaining(self):
        #allows us to initialize the lenRemaining of the first word
        if ( self.storage[self.activeWordIndex] >> np.uint64(63) ) == 1:
            #if fill word get the length of it
            self.lenRemaining = self.storage[self.activeWordIndex] & ~( np.uint64(3) << np.uint64(62) )
        else:
            #if literal just set to 0
            self.lenRemaining = 0;

    def getLen(self):
        #gets the length of the run word 
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

    def getTotalLength(self):

        totalLength = 0

        for i in range(len(self.storage)):
            runOrLiteral = self.storage[i] >> np.uint64(63)
            if runOrLiteral == 1:
                #Is run
                length = self.storage[i] & ~(np.uint64(3) << np.uint64(62))
                totalLength += length
            else:
                #Is literal
                totalLength += 1
        return totalLength


    def printBitVector(self):
        for i in self.storage:
            print np.binary_repr(i, width = 64)

    def isLiteral(self, word):
        return word >> self.wordSizeInBits - np.uint64(1) == 0

    def setBitInActiveWord(self,pos,bit):
        if bit == 0:
            self.storage[self.appendWordIndex] &= ~(np.uint64(1)<<(np.uint64(self.wordSizeInBits - 2) - np.uint64(pos)))
        else:
            self.storage[self.appendWordIndex] |=  (np.uint64(1)<<(np.uint64(self.wordSizeInBits - 2) - np.uint64(pos)))
    
    # Make sure that lenInWords can fit in the current storage
    def ensureStorageFits(self, lenInWords):
        if self.storage.size < lenInWords:
            # TODO: In the future, this should do something a bit more efficient, like growing in blocks of size 1.5*current length or something like that.
            self.storage.resize(lenInWords)       

    def appendWord(self, word):
        #appends a word to a bitVector based on logical operations
        #Will also check if word is a run and send it to appendRun which will add it
    
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
            #Checks if length is too big to add to current run
            while (self.storage[self.activeWordIndex - 1] & ~(np.uint64(3) << np.uint64(62))) <= 4611686018427387903:
                #Adds one to the length 
                self.storage[self.activeWordIndex - 1] += length
            #If run becomes too large it will create an new run in the next spot in storage
            self.ensureStorageFits(self.activeWordIndex + 1)
            newRun = np.uint64(1) << np.uint64(63)
            newRun += np.uint64(runType) << np.uint64(62)
            newRun += 1
            self.storage[self.activeWordIndex] = newRun
            
        else:
            self.ensureStorageFits(self.activeWordIndex + 1)        
            
            self.storage[self.activeWordIndex] = word
            
            self.activeWordIndex += 1
    
    #######################################################################
    #                           Methods                                   #
    #######################################################################
        
    def __init__(self):

        #Creates bitVector
        self.storage = np.zeros(1,dtype = np.uint64)
        
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
        
        self.appendWordIndex = 0 # Location of the last word in the bitvector. The append function will *only* work with this index

        #lenRemaining is the lenght of the fill word
        self.lenRemaining = 0
        
        # Location of the last word in the bitvector. The append function will *only* work with this index.
        self.appendWordIndex = 0 
        
        #totallength
        self.totalLength = 0
    
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
        if self.getTotalLength() != other.getTotalLength():
            print "Not Same Size. Error."
            return
        
        #Sets activeWordIndex to zero for both self and other
        self.activeWordIndex = 0
        other.activeWordIndex = 0

        #Creates new bitVector to hold xor operation
        new = bitVector()
        self.totalLength = self.getTotalLength()
        
        #FIXME: Not sure how to iterate this 
        while self.totalLength:
            
            #checks for cases
            selfCheck = self.storage[self.activeWordIndex] >> np.uint64(63)
            otherCheck = other.storage[other.activeWordIndex] >> np.uint64(63)
            
            #Case 1: Both are literals
            if selfCheck == otherCheck and selfCheck == 0:
                #XOR operation done between the two current words
                newWrd = self.storage[self.activeWordIndex] ^ other.storage[other.activeWordIndex]
                #Adds the XOR'ed word to the new bitVector
                new.appendWord(newWrd)
                #Since we used these two words, we subtract one from each of the total lengths 
                self.totalLength -= 1
                #Moves the iterator forward for each bitVector (since both literals we move each by one word)
                self.moveIteratorForward(1)
                other.moveIteratorForward(1)
                
            #Case 2: Both are fills
            if selfCheck == otherCheck and selfCheck == 1:
                #Gets the length of the two fills 
                getLength = np.uint64(1) << np.uint64(63)
                getLength += np.uint64(1) << np.uint64(62)
                selfLength = self.storage[self.activeWordIndex] & ~(getLength)
                otherLength = other.storage[other.activeWordIndex] & ~(getLength)
                        
                #Gets whether the runs are runs of one's or zero's
                selfRunType = (self.storage[self.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                otherRunType = (other.storage[other.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                #If the runtypes are equal (1 == 1 or 0 == 0)
                if selfRunType == otherRunType and (selfRunType == 1 or selfRunType == 0):
                    new.appendRun(0,totalLength)
                #If the runtypes are not equal
                if selfRunType != otherRunType:
                    new.appendRun(1,totalLength)
                #Checks which run is smaller
                if selfLength > otherLength:
                    self.moveIteratorForward(otherLength)
                    other.moveIteratorForward(otherLength)
                    self.totalLength -= otherLength
                if otherLength > selfLength:
                    self.moveIteratorForward(selfLength)
                    other.moveIteratorForward(selfLength)
                    self.totalLength -= selfLength
                #If same size
                else:
                    self.moveIteratorForward(selfLength)
                    other.moveIteratorForward(otherLength)
                    self.totalLength -= selfLength
                


            #Case 3: One is literal and one is run
            if selfCheck != otherCheck and (selfCheck == 0 or otherCheck == 0):
                #If self is a run
                if selfCheck == 1:
                    #Gets self's runtype
                    selfRunType = (self.storage[self.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                    #If run of ones
                    if selfRunType == 1:
                        #Creates a literal of ones to be XOR'ed (first bit doesn't matter)
                        tmpWrd = ~(np.uint64(1) << np.uint64(63))
                    #Run of zeros
                    else:
                        #Creates a literal of zeros to be XOR'ed (first bit doesn't matter)
                        tmpWrd = np.uint64(1) << np.uint64(63)
                        
                    newWrd = other.storage[other.activeWordIndex] ^ tmpWrd
                    newWrd &= ~(np.uint64(1) << np.uint64(63))
                    new.appendWord(newWrd)
                    
                #If other is run
                if otherCheck == 1:
                    #Get other's runtype
                    otherRunType = (other.storage[other.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                    #If runtype is run of ones
                    if otherRunType == 1:
                        #Creates a literal of ones to be XOR'ed (first bit doesn't matter)
                        tmpWrd = ~(np.uint64(1) << np.uint64(63))
                    #Run of zeros
                    else:
                        #Creates a literal of zeros to be XOR'ed (first bit doesn't matter)
                        tmpWrd = np.uint64(1) << np.uint64(63)
                        
                    newWrd = self.storage[self.activeWordIndex] ^ tmpWrd
                    newWrd &= ~(np.uint64(1) << np.uint64(63))
                    new.appendWord(newWrd)
                #Moves iterator forward and it will track run length
                self.moveIteratorForward(1)
                other.moveIteratorForward(1)
                self.totalLength -= 1
            
        #Sets the bitVector's storage equal to the XOR'ed bitVector
        self.storage = new.storage

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
            if selfCheck == 0 and otherCheck == 0:
                newWrd = self.storage[self.activeWordIndex] | other.storage[other.activeWordIndex]
                newWrd &= ~(np.uint64(1) << np.uint64(63))
                
                new.appendWord(newWrd)
        
                self.moveIteratorForward(1)
                other.moveIteratorForward(1)
                
            #Case 2: Both are runs
            if selfCheck == 1 and otherCheck == 1:
                
                #Determines whether run is of 1's or 0's
                selfRunType = (self.storage[self.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                otherRunType = (other.storage[other.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                
                #Determines overlapping length between the two runs
                if self.lenRemaining > other.lenRemaining:
                    overlapLength = other.lenRemaining
                if self.lenRemaining < other.lenRemaining:
                    overlapLength = self.lenRemaining
                elif self.lenRemaining == other.lenRemaining:
                    overlapLength = self.lenRemaining

                #Conducts OR operation between the two runs
                if selfRunType == otherRunType:
                    new.appendRun(selfRunType, overlapLength)
                    self.moveIteratorForward(overlapLength)
                    other.moveIteratorForward(overlapLength)
                elif (selfRunType == 1 and otherRunType == 0) or (selfRunType == 0 and otherRunType == 1):
                    new.appendRun(1, overlapLength)
                    self.moveIteratorForward(overlapLength)
                    other.moveIteratorForward(overlapLength)
                
            #Case 3: One is a literal, one is a run
            if selfCheck != otherCheck:
                #Determines whether potential runs are of 1's or 0's
                selfRunType = (self.storage[self.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                otherRunType = (other.storage[other.activeWordIndex] >> np.uint64(62)) & np.uint64(1)

                #Determines which bitVector is a run and which is a literal
                if selfCheck == 1 and otherCheck == 0:
                    if selfRunType == 0:
                        new.appendWord(other.storage(other.activeWordIndex))
                        self.moveIteratorForward(1)
                        other.moveIteratorForward(1)
                    elif selfRunType == 1:
                        new.appendRun(selfRunType, self.lenRemaining)
                        self.moveIteratorForward(self.lenRemaining)
                        other.moveIteratorForward(self.lenRemaining)

                elif selfCheck == 0 and otherCheck == 1:
                    if otherRunType == 0:
                        new.appendWord(self.storage(self.activeWordIndex))
                        self.moveIteratorForward(1)
                        other.moveIteratorForward(1)
                    elif otherRunType == 1:
                        new.appendRun(otherRunType, other.lenRemaining)
                        self.moveIteratorForward(other.lenRemaining)
                        other.moveIteratorForward(other.lenRemaining)
                    
                
    def AND(self, other):
        ############ REMINDER #############
        #   anything '&' with 0 is zero   #
        #anything '&' with 1 is that thing#
        ###################################
        
        # Make sure we are starting with the first word
        self.activeWordIndex = 0
        other.activeWordIndex = 0

        #create a new bit vector to store the result 
        new = bitVector()
        
        self.getFirstLenRemaining()
        other.getFirstLenRemaining()

        #Since our bit vectors will be of the same length we can just keep
        #track of the length of self we will update loopLen whenever we update
        #self.activeWordIndex
        loopLen = self.getTotalLength()
        
        ##########
        # Fix Me #
        ##########

        while (loopLen != 0):

            # use bit shifting to see if we have fill words or literal words
            msbSelf = self.storage[self.activeWordIndex] >> np.uint64(63) 
            msbOther = other.storage[other.activeWordIndex] >> np.uint64(63)  

            #Case 1: if both are fill
            if msbSelf == 1 and msbOther == 1:
                #find what kind of fills we are dealing with
                selfRunType = self.storage[self.activeWordIndex] & ( np.uint64(1) << np.uint64(62) )
                otherRunType = other.storage[other.activeWordIndex] & ( np.uint64(1) << np.uint64(62) )

                #find the length of the fills
                selfLen = self.lenRemaining
                otherLen = other.lenRemaining

                #if both are fills of 0's iterate by the larger length
                if selfRunType == 0 and otherRunType == 0:

                    #if SELF is a longer fill than OTHER
                    if selfLen > otherLen:
                        #iterate OTHER by selfLen
                        other.moveIteratorForward(selfLen)

                        #add the SELF fill word to the new Bit Vector
                        new.appendWord( self.storage[self.activeWordIndex] )

                        #move onto the next word in SELF
                        self.moveIteratorForward(1)
                        
                        #update loopLen
                        loopLen -= 1
                        
                    #if OTHER is a longer fill than SELF
                    else:
                        #iterate SELF by otherLen
                        self.moveIteratorForward(otherLen)

                        #add the OTHER fill word to new Bit Vector
                        new.appendWord( other.storage[other.activeWordIndex] )

                        #move onto the next word in OTHER
                        other.moveIteratorForward(1)
                        
                        #update loopLen
                        loopLen -= otherLen

                #if only SELF is a fill of 0's
                elif selfRunType == 0:
                    #move OTHER by selfLen
                    other.moveIteratorForward(selfLen)  

                    #add the fill of 0's to new Bit Vector                  
                    new.appendWord( self.storage[self.activeWordIndex] )

                    #move onto the next word of SELF
                    self.moveIteratorForward(1)
                    
                    #update loopLen
                    loopLen -= 1

                #if only OTHER is a fill of 0's
                elif otherRunType == 0:
                    #move SELF by otherLen
                    self.moveIteratorForward(otherLen)

                    #add the fill of 0's to new Bit Vector 
                    new.appendWord( other.storage[other.activeWordIndex] )

                    #move onto the next word of OTHER
                    other.moveIteratorForward(1)
                    
                    #update loopLen
                    loopLen -= otherLen
                
                #if both are fills of 1's
                else:
                    #if OTHER is longer
                    if otherLen > selfLen:
                        #move OTHER by the amount of selfLen
                        other.moveIteratorForward(selfLen)

                        #append SELF to the new Bit Vector
                        new.appendWord( self.storage[self.activeWordIndex] )

                        #move SELF to the next word
                        self.moveIteratorForward(1)
                        
                        #update loopLen
                        loopLen -= 1

                    #if SELF is longer
                    else:
                        #move SELF by the amount of otherLen
                        self.moveIteratorForward(otherLen)

                        #append OTHER to the new Bit Vector
                        new.appendWord( other.storage[other.activeWordIndex] )

                        #move OTHER to the next word
                        other.moveIteratorForward(1)
                        
                        #update loopLen
                        loopLen -= otherLen

                    
            #Case 2: if only SELF is a fill
            elif msbSelf == 1:

                #find if its a fill of 0's or 1's
                selfRunType = self.storage[self.activeWordIndex] & ( np.uint64(1) << np.uint64(62) )

                #find the length of the fill
                selfLen = self.lenRemaining

                #if the fill is of 0's than just write the fill
                if selfRunType == 0:
                    other.moveIteratorForward(selfLen)
                    new.appendWord( self.storage[self.activeWordIndex] )
                    self.moveIteratorForward(selfLen)
                    
                    #update loopLen
                    loopLen -= selfLen

                #if the fill is of 1's than iterate through 
                else:
                    #creating a variable that will help us later
                    msbOther = 0

                    for i in range(selfLen):
                        #check to see if we incounter a fill of 0's, break if we do and change the
                        #the remaining length of SELF with repsect to how many times we have looped
                        if msbOther == 1 :
                            break

                        else:
                            #since anything '&' with 1 is itself we can just add the OTHER word
                            new.appendWord(other.storage[other.activeWordIndex])

                            #increase activeWordIndex since we know that OTHER is a literal word
                            other.moveIteratorForward(1)

                            #update OTHER so we can check if we run into a fill word
                            msbOther = other.storage[other.activeWordIndex] >> np.uint64(63)
                            
                            #update self.lenRemaining
                            self.moveIteratorForward(1)
                            
                            loopLen -= 1
                            
                        
                    
            #Case 3: if only OTHER is a fill
            elif msbOther == 1:
                #find if its a fill of 0's or 1's
                otherRunType = other.storage[other.activeWordIndex] & ( np.uint64(1) << np.uint64(62) )
                                
                #find the length of the fill
                otherLen = other.lenRemaining

                #if the fill is of 0's than just write the fill and move OTHER to 
                #the next word
                if otherRunType == 0:
                    self.moveIteratorForward(otherLen)
                    new.appendWord( other.storage[other.activeWordIndex] )
                    other.moveIteratorForward(otherLen)
                    
                    #update loopLen
                    loopLen -= otherLen

                #if the fill is of 1's than iterate through 
                else:
                    #creating a variable that will help us later
                    msbSelf = 0

                    for i in range(otherLen):
                        #check to see if we incounter a fill of 0's, break if we do and change the
                        #the remaining length of OTHER with repsect to how many times we have looped
                        if msbSelf == 1 :
                            break

                        else:
                            #since anything '&' with 1 is itself we can just add the SELF word
                            new.appendWord(self.storage[self.activeWordIndex])

                            #increase activeWordIndex since we know that SELF is a literal word
                            self.moveIteratorForward(1)
                            
                            #update loopLen
                            loopLen -= 1 

                            #update SELF so we can check if we run into a fill word
                            msbSelf = self.storage[self.activeWordIndex] >> np.uint64(63)                             
                            
                            #update other.lenRemaining
                            other.moveIteratorForward(1)
                    

            #Case 4: if both are literals
            else:
                #since both are literal we can just do a bitwise '&' on them and store that into our new Bit Vector
                new.appendWord( self.storage[self.activeWordIndex] & other.storage[other.activeWord] )

                #move onto the next word
                self.moveIteratorForward(1)
                other.moveIteratorForward(1)
                
                #update loopLen
                loopLen -= 1




