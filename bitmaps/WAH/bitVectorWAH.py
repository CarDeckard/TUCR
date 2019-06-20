import numpy as np
from WAHStorageWordBuilder import WAHStorageWordBuilder
from WAHStorageWordIterator import WAHStorageWordIterator

class bitVectorWAH(object):
    
    ## Initialize the bitVector with an appropriate storage.
    def __init__(self, wahStorage = WAHStorageWordBuilder()):
        self.wahStorage = wahStorage

    #######################################################################
    #                         Helper Functions                            #
    #######################################################################
    
    ## NOTE: I partially modified this, to use the new iterator. You need to fix the rest.
    def xor(self, other):
        #Checks if Bit Vectors are same size (throws error if not)
        if self.wahStorage.totalLength != other.wahStorage.totalLength:
            raise Exception("Not the same size.")
        
        # These are the iterators which
        me = WAHStorageWordIterator(self.wahStorage)
        you = WAHStorageWordIterator(other.wahStorage)

        #Creates new bitVector to hold xor operation
        new = WAHStorageWordBuilder()
        
        while not (me.isDone() or you.isDone()):
            (meActiveWord, meLenRemaining) = me.current()
            (youActiveWord, youLenRemaining) = you.current()
            
            meLiteral = me.wahStorage.isLiteral(meActiveWord)
            youLiteral = you.wahStorage.isLiteral(youActiveWord)
            
            #Case 1: Both are literals
            # NOTE: This is the one I modified.
            if meLiteral and youLiteral:
                #XOR operation done between the two current words
                newWrd = meActiveWord ^ youActiveWord
                #Adds the XOR'ed word to the new bitVector
                new.appendWord(newWrd)
                
                #Moves the iterator forward for each bitVector (since both literals we move each by one word)
                me.moveIteratorForward(1)
                you.moveIteratorForward(1)
                
            #Case 2: Both are fills
            # FIXME: I only modified the if statement. You need to fix up the rest.
            elif (not meLiteral) and (not youLiteral):
                ######XOR of Runs Table######
                # A # B ################ Z ##
                #--------------------------##
                # 0 # 0 ################ 0 ##
                # 0 # 1 ################ 1 ##
                # 1 # 0 ################ 1 ##
                # 1 # 1 ################ 0 ##
                #############################
                #Gets the run types for me and you to determine the fill that will be appended
                meRunType = me.wahStorage.getRunType(meActiveWord)
                youRunType = you.wahStorage.getRunType(youActiveWord)
                #Gets length of current word                
                meLength = me.wahStorage.getRunLen(meActiveWord)
                youLength = you.wahStorage.getRunLen(youActiveWord)
                #Compares length the determine how to iterate
                if meLength == youLength:
                    appendLength = meLength
                else:
                    if meLength > youLength:
                        appendLength = youLength
                    else:
                        appendLength = meLength
                
                #compares runtypes and decides what to append
                if meRunType == youRunType:
                    new.appendRun(0,appendLength)
                else:
                    new.appendRun(1,appendLength)
                    
                #Move iterator by the smaller size
                me.moveIteratorForward(appendLength)
                you.moveIteratorForward(appendLength)                

            #Case 3: One is literal and one is run
            # FIXME: I only modified the if statement. You need to fix up the rest.
            else:
                #If me is literal (you is run)
                if meLiteral:
                    youRunType = you.wahStorage.getRunType(youActiveWord)
                    
                    if youRunType == 0:
                        new.appendRun(0,1)
                    else:
                        tmpWrd = 
                    
            
        #Sets the bitVector's storage equal to the XOR'ed bitVector
        self.storage = new.storage

    ## FIXME: I have not modified this to use the new iterator. You need to do so. See xor function for hints.
    def Or(self, other):
        
        new = bitVector()

        #Checks that vectors are the same size
        if self.numRows != other.numRows:
            print "Error: Vectors are of unequal size"
            return
        
        #sets activeWordIndex to zero for both self and other
        self.activeWordIndex = 0
        other.activeWordIndex = 0
        
        #Since our bit vectors will be of the same length we can just keep
        #track of the length of self we will update loopLen whenever we update
        #self.activeWordIndex
        loopLen = self.getTotalLength()
        
        for i in range(loopLen):
            
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
                
                loopLen -= 1
                
            #Case 2: Both are runs
            if selfCheck == 1 and otherCheck == 1:
                
                #Determines whether run is of 1's or 0's
                selfRunType = (self.storage[self.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                otherRunType = (other.storage[other.activeWordIndex] >> np.uint64(62)) & np.uint64(1)
                
                #Determines overlapping length between the two runs
                if self.lenRemaining > other.lenRemaining:
                    overlapLength = other.lenRemaining
                else:
                    overlapLength = self.lenRemaining


                #Conducts OR operation between the two runs
                if selfRunType == otherRunType:
                    new.appendRun(selfRunType, overlapLength)
                    self.moveIteratorForward(overlapLength)
                    other.moveIteratorForward(overlapLength)
                    
                    loopLen -= overlapLength
                    
                elif (selfRunType == 1 and otherRunType == 0) or (selfRunType == 0 and otherRunType == 1):
                    new.appendRun(1, overlapLength)
                    self.moveIteratorForward(overlapLength)
                    other.moveIteratorForward(overlapLength)
                    
                    loopLen -= overlapLength
                
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
                        
                        loopLen -= 1
                        
                    elif selfRunType == 1:
                        new.appendRun(selfRunType, self.lenRemaining)
                        self.moveIteratorForward(self.lenRemaining)
                        other.moveIteratorForward(self.lenRemaining)
                        
                        loopLen -= self.lenRemaining

                elif selfCheck == 0 and otherCheck == 1:
                    if otherRunType == 0:
                        new.appendWord(self.storage(self.activeWordIndex))
                        self.moveIteratorForward(1)
                        other.moveIteratorForward(1)
                        
                        loopLen -= 1
                        
                    elif otherRunType == 1:
                        new.appendRun(otherRunType, other.lenRemaining)
                        self.moveIteratorForward(other.lenRemaining)
                        other.moveIteratorForward(other.lenRemaining)
                        
                        loopLen -= other.lenRemaining
                    
    ## FIXME: I have not modified this to use the new iterator. You need to do so. See xor function for hints.
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
                new.appendWord( self.storage[self.activeWordIndex] & other.storage[other.activeWordIndex] )

                #move onto the next word
                self.moveIteratorForward(1)
                other.moveIteratorForward(1)
                
                #update loopLen
                loopLen -= 1




