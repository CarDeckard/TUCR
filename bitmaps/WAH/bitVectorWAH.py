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

        ##########XOR Table##########
        # A # B ################ Z ##
        #--------------------------##
        # 0 # 0 ################ 0 ##
        # 0 # 1 ################ 1 ##
        # 1 # 0 ################ 1 ##
        # 1 # 1 ################ 0 ##
        #############################        
        
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
                        new.appendWord(~(meActiveWord))
                if youLiteral:
                    meRunType = me.wahStorage.getRunType(meActiveWord)
                    
                    if meRunType == 0:
                        new.appendRun(0,1)
                    else:
                        new.appendWord(~(youActiveWord))
                    
            
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

        #Checks if Bit Vectors are same size (throws error if not)
        if self.wahStorage.totalLength != other.wahStorage.totalLength:
            raise Exception("Not the same size.")
        
        # These are the iterators which
        me = WAHStorageWordIterator(self.wahStorage)
        you = WAHStorageWordIterator(other.wahStorage)

        #Creates new bitVector to hold xor operation
        new = WAHStorageWordBuilder()        

        while not ( me.isDone() or you.isDone() ):
            (meActiveWord, meLenRemaining) = me.current()
            (youActiveWord, youLenRemaining) = you.current()
            
            meLiteral = me.wahStorage.isLiteral(meActiveWord)
            youLiteral = you.wahStorage.isLiteral(youActiveWord)
            
            #Case 1: Both are literals
            if meLiteral and youLiteral:
                #AND operation done between the two current words
                newWrd = meActiveWord & youActiveWord
                #Adds the AND'ed word to the new bitVector
                new.appendWord(newWrd)
                
                #Moves the iterator forward for each bitVector
                me.moveIteratorForward(1)
                you.moveIteratorForward(1)
            
            #Case 2: Both are fills
            elif (not meLiteral) and (not youLiteral):
                
                #Get the run type of both BV
                meType = me.getRunType(meLiteral)
                youType = you.getRunType(youLiteral)
                
                #If both are runs of 0's
                if meType == 0 and youType == 0:
                    #If me is a longer run than you
                    if meLenRemaining > youLenRemaining:
                        
                        ## FIXME :add in appending functions
                        newWrd = meActiveWord
                        
                        #Adds the AND'ed word to the new bitVector
                        new.appendWord(newWrd)
                        
                        #Moves the iterator forward for each bit vector by the run length of me
                        me.moveIteratorForward(meLenRemaining)
                        you.moveIteratorForward(meLenRemaining)
                        
                    #If they are the same size or you is the longer run
                    else:
                        
                        ## FIXME :add in appending functions
                        newWrd = youActiveWord
                        
                        #Adds the AND'ed word to the new bitVector
                        new.appendWord(newWrd)
                        
                        #Moves the iterator forward for each bit vector by the run length of you
                        me.moveIteratorForward(youLenRemaining)
                        you.moveIteratorForward(youLenRemaining)
                        
                    
                #If only me is a run of 0's
                elif meType == 0:
                    
                    ## FIXME :add appending functions
                    newWrd = meActiveWord
                    
                    #Adds the AND'ed word to the new bitVector
                    new.appendWord(newWrd)
                    
                    #Moves the iterator forward for each bit vector by the run length of me
                    me.moveIteratorForward(meLenRemaining)
                    you.moveIteratorForward(meLenRemaining)  
                    
                #If only you is a run of 0's
                elif youType == 0:
                    
                    ## FIXME :add appending functions
                    newWrd = youACtiveWord
                    
                    #Adds the AND'ed word to the new bitVector
                    new.appendWord(newWrd)
                    
                    #Moves the iterator forward for each bit vector by the run length of you
                    me.moveIteratorForward(youLenRemaining)
                    you.moveIteratorForward(youLenRemaining) 
                    
                #If both are runs of 1's
                else:
                    
                    if meLenRemaining > youLenRemaining:
                        
                        ## FIXME :add in appending functions
                        
                        #Adds the AND'ed word to the new bitVector
                        new.appendWord(newWrd)
                        
                        #Moves the iterator forward for each bit vector by the run length of you
                        me.moveIteratorForward(youLenRemaining)
                        you.moveIteratorForward(youLenRemaining)
                        
                    #If they are the same size or you is the longer run
                    else:
                        
                        ## FIXME :add in appending functions
                        
                        #Adds the AND'ed word to the new bitVector
                        new.appendWord(newWrd)
                        
                        #Moves the iterator forward for each bit vector by the run length of me
                        me.moveIteratorForward(meLenRemaining)
                        you.moveIteratorForward(meLenRemaining)
                    
            #Case 3: One is literal and one is run
            else:
                
                #If me is the run
                if (not meLiteral):
                    #Get the run type of me
                    meType = me.getRunType(meLiteral)
                    
                    #If me is a run of 0's append the run of 0's and iterate by meLenRemaining
                    if meType == 0:
                        
                        ## FIXME :append me 
                        
                        #Adds the AND'ed word to the new bitVector
                        new.appendWord(newWrd)
                        
                        #Iterate both by the length of the run of 0's
                        me.moveIteratorForward(meLenRemaining)
                        you.moveIteratorForward(meLenRemaining)
                    
                    #Else me is a run of 1's and we should append the literal and iterate both by one word
                    else:
                        
                        ## FIXME :append literal word
                        
                        #Adds the AND'ed word to the new bitVector
                        new.appendWord(newWrd)
                        
                        #Iterate both to the next word
                        me.moveIteratorForward(1)
                        you.moveIteratorForward(1)
                    
                #If you is the run
                else:
                    #Get the run type of you
                    youType = you.getRunType(youLiteral)
                
                    #If me is a run of 0's append the run of 0's and iterate by meLenRemaining
                    if youType == 0:
                        
                        ## FIXME :append me 
                        
                        #Adds the AND'ed word to the new bitVector
                        new.appendWord(newWrd)
                        
                        #Iterate both by the length of the run of 0's
                        me.moveIteratorForward(youLenRemaining)
                        you.moveIteratorForward(youLenRemaining)
                        
                    
                    #Else you is a run of 1's and we should append the literal and iterate both by one word
                    else:
                        
                        ## FIXME :append literal word
                        
                        #Adds the AND'ed word to the new bitVector
                        new.appendWord(newWrd)
                        
                        #Iterate both to the next word 
                        me.moveIteratorForward(1)
                        you.moveIteratorForward(1)
                        

