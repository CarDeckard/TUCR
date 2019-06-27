import sys
sys.path.append('..')
from ABCBitVector import ABCBitVector
from WAHStorageWordBuilder import WAHStorageWordBuilder
from WAHStorageBitBuilder import WAHStorageBitBuilder
from WAHStorageWordIterator import WAHStorageWordIterator

class bitVectorWAH(ABCBitVector):
    
    ## Initialize the bitVector with an appropriate storage.
    def __init__(self, wahStorage = None):
        if wahStorage is None:
            wahStorage = WAHStorageBitBuilder()
        super(bitVectorWAH, self).__init__(wahStorage)

    #######################################################################
    #                         Helper Functions                            #
    #######################################################################
    def append(self,bit):
        self.baseStorage.append(bit)
    
    ## FIXME: Doesn't work if rows are out of order! See WAHStorageBitBuilder
    def add(self,row):
        self.baseStorage.addSequential(row)
        
        
    def COUNT(self):
        # Adds up all of the 1's in the BitVector to find where we have hits
        numCount = 0
        
        # Our iterator for this function 
        me = WAHStorageWordIterator(self.baseStorage)
                
        while not me.isDone():
                                    
            (meActiveWord, meLenRemaining) = me.current()
            
            meLiteral = me.wahStorage.isLiteral(meActiveWord)

            # If the word is a literal 
            if meLiteral:
                
                #Iterate through every bit one by one and count only if it is 
                #equal to 1 then move onto the next bit 
                for i in range(63):
                    bit = ( int(meActiveWord) >> i ) & 1
                    
                    if bit == 1:
                        numCount += 1
                        
                me.moveIteratorForward(1)  
                
            # If the word is a fill
            else:
                
                #If the run is of 1's than add all of the 1's in the run
                meRunType = me.wahStorage.getRunType(meActiveWord)
                
                if meRunType == 1:
                    
                    #Since each word can only hold 63 we have 63 times the
                    #length of the fill
                    numCount += 63 * (meLenRemaining + 1)
                    
                me.moveIteratorForward(meLenRemaining + 1)                
                    
        return numCount
                
        
    
    
        
    def XOR(self, other):

        ##########XOR Table##########
        # A # B ################ Z ##
        #--------------------------##
        # 0 # 0 ################ 0 ##
        # 0 # 1 ################ 1 ##
        # 1 # 0 ################ 1 ##
        # 1 # 1 ################ 0 ##
        #############################        
        
        #Checks if Bit Vectors are same size (throws error if not)
        if self.baseStorage.totalLength != other.baseStorage.totalLength:
            raise Exception("Not the same size.")
        
        # These are the iterators which
        me = WAHStorageWordIterator(self.baseStorage)
        you = WAHStorageWordIterator(other.baseStorage)

        #Creates new bitVector to hold xor operation
        new = WAHStorageWordBuilder()
        
        while not (me.isDone() or you.isDone()):
            (meActiveWord, meLenRemaining) = me.current()
            (youActiveWord, youLenRemaining) = you.current()
            
            meLiteral = me.wahStorage.isLiteral(meActiveWord)
            youLiteral = you.wahStorage.isLiteral(youActiveWord)
        
            
            #Case 1: Both are literals
            if meLiteral and youLiteral:
                
                #XOR operation done between the two current words
                newWrd = meActiveWord ^ youActiveWord
                #Adds the XOR'ed word to the new bitVector
                new.appendWord(newWrd)
                
                #Moves the iterator forward for each bitVector (since both literals we move each by one word)
                me.moveIteratorForward(1)
                you.moveIteratorForward(1)
                
            #Case 2: Both are fills
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
                #Compares length then determines how to iterate
                if meLength == youLength:
                    appendLength = meLength
                else:
                    if meLength > youLength:
                        appendLength = youLength
                    else:
                        appendLength = meLength
                
                #Compares runtypes and decides what to append
                if meRunType == youRunType:
                    new.appendRun(0,appendLength)
                else:
                    new.appendRun(1,appendLength)
                    
                #Move iterator by the smaller size
                me.moveIteratorForward(appendLength)
                you.moveIteratorForward(appendLength)                

            #Case 3: One is literal and one is run
            else:
                #If me is literal (you is run)
                if meLiteral:
                    youRunType = you.wahStorage.getRunType(youActiveWord)
                    
                    if youRunType == 0:
                        new.appendRun(0,1)
                    else:
                        
                        # XOR with a run of 1's is equivalent to getting the compliment
                        # of the what is being XOR'ed. We have to make sure that we are
                        # not touching the most significant bit though because it is
                        # always going to be a run
                        newWrd = ~(meActiveWord) & (~(1 << 63))
                        
                        new.appendWord(newWrd)
                    
                    me.moveIteratorForward(1)
                    you.moveIteratorForward(1)
                
                #If you is literal (me is run)
                if youLiteral:
                    meRunType = me.baseStorage.getRunType(meActiveWord)
                    
                    if meRunType == 0:
                        new.appendRun(0,1)
                    else:
                        new.appendWord(~(youActiveWord))
                    me.moveIteratorForward(1)
                    you.moveIteratorForward(1)
                    
        return bitVectorWAH(new)

    def OR(self, other):
        
                ########## OR Table #########
                # A # B ################ Z ##
                #--------------------------##
                # 0 # 0 ################ 0 ##
                # 0 # 1 ################ 1 ##
                # 1 # 0 ################ 1 ##
                # 1 # 1 ################ 1 ##
                #############################  

        #Checks if Bit Vectors are same size (throws error if not)
        if self.baseStorage.totalLength != other.baseStorage.totalLength:
            raise Exception("Not the same size.")

        # These are the iterators which
        me = WAHStorageWordIterator(self.baseStorage)
        you = WAHStorageWordIterator(other.baseStorage)

        #Creates new bitVector to hold or operation
        new = WAHStorageWordBuilder()
    
        while not (me.isDone() or you.isDone()):
            (meActiveWord, meLenRemaining) = me.current()
            (youActiveWord, youLenRemaining) = you.current()
            
            meLiteral = me.wahStorage.isLiteral(meActiveWord)
            youLiteral = you.wahStorage.isLiteral(youActiveWord) 

            #Case 1: Both are literals
            if meLiteral and youLiteral:                
                #OR operation done between  the two current words
                newWrd = meActiveWord | youActiveWord
                #adds the OR'ed word to the new bitVector
                new.appendWord(newWrd)
                #Moves the iterator forward for each bitVector (since both literals, we move each by one word)
                me.moveIteratorForward(1)
                you.moveIteratorForward(1)
                
            #Case 2: Both are runs

            elif (not meLiteral) and (not youLiteral):
                #gets the run types for me and you to determine the fill that will be appended
                meRunType = me.wahStorage.getRunType(meActiveWord)
                youRunType = you.wahStorage.getRunType(youActiveWord)

                #Gets the length of the current word
                meLength = me.wahStorage.getRunLen(meActiveWord)
                youLength = you.wahStorage.getRunLen(youActiveWord)

                #Compares length and then determines how to iterate
                if meLength == youLength:
                    appendLength = meLength
                else:
                    if meLength > youLength:
                        appendLength = youLength
                    else:
                        appendLength = meLength
                
                #Compares runtypes and decides what to append
                if meRunType == 0 and youRunType == 0:
                    new.appendRun(0, appendLength)
                elif meRunType == 1 and youRunType == 0:
                    appendLength = meLength
                    new.appendRun(1, meLength)
                elif meRunType == 0 and youRunType == 1:
                    appendLength = youLength
                    new.appendRun(1, appendLength)

                #Move iterator by the smaller size
                me.moveIteratorForward(appendLength)
                you.moveIteratorForward(appendLength)
    
            #Case 3: One is a literal, one is a run

            else:
                #If me is literal (you is run)
                if meLiteral:
                    #Determines run type and length
                    youRunType = you.baseStorage.getRunType(youActiveWord)
                    youLength = you.baseStorage.getRunLen(youActiveWord)

                    if youRunType == 0:
                        appendLength = 1
                        new.appendWord(meActiveWord)
                    else:
                        appendLength = youLength
                        new.appendRun(1, appendLength)

                #If you is literal (me is run)
                elif youLiteral:
                    #Determines run type and length
                    meRunType = me.baseStorage.getRunType(meActiveWord)
                    meLength = me.baseStorage.getRunLen(meActiveWord)

                    if meRunType == 0:
                        appendLength = 1
                    if meRunType == 0:
                        new.appendRun(youActiveWord)
                    else:
                        appendLength = meLength
                        new.appendWord(1, appendLength)

                #Moves iterator forward for each bitVector
                me.moveIteratorForward(appendLength)
                you.moveIteratorForward(appendLength)

        return bitVectorWAH(new)
                    
    def AND(self, other):
        
                ########## AND Table #########
                # A # B ################# Z ##
                #---------------------------##
                # 0 # 0 ################# 0 ##
                # 0 # 1 ################# 0 ##
                # 1 # 0 ################# 0 ##
                # 1 # 1 ################# 1 ##
                ############################## 

        #Checks if Bit Vectors are same size (throws error if not)
        if self.baseStorage.totalLength != other.baseStorage.totalLength:
            raise Exception("Not the same size.")
        
        # These are the iterators which
        me = WAHStorageWordIterator(self.baseStorage)
        you = WAHStorageWordIterator(other.baseStorage)

        #Creates new bitVector to hold AND operation
        new = WAHStorageWordBuilder()        

        while not ( me.isDone() or you.isDone() ):
                        
            (meActiveWord, meLenRemaining) = me.current()
            (youActiveWord, youLenRemaining) = you.current()
            
            meLiteral = me.wahStorage.isLiteral(meActiveWord)
            youLiteral = you.wahStorage.isLiteral(youActiveWord)
            
            #
            #Case 1: Both are literals
            #
            if meLiteral and youLiteral:
                                
                #AND operation done between the two current words
                newWrd = meActiveWord & youActiveWord
                #Adds the AND'ed word to the new bitVector
                new.appendWord(newWrd)
                                
                #Moves the iterator forward for each bitVector
                me.moveIteratorForward(1)
                you.moveIteratorForward(1)
            
            #
            #Case 2: Both are fills
            #
            elif (not meLiteral) and (not youLiteral):
                                
                #Get the run type of both BV
                meType = me.wahStorage.getRunType(meLiteral)
                youType = you.wahStorage.getRunType(youLiteral)
                
                #If both are runs of 0's
                if meType == 0 and youType == 0:
                    
                    #If me is a longer run than you
                    if meLenRemaining > youLenRemaining:
                                                
                        #Adds the AND'ed word to the new bitVector
                        new.appendRun( meType , meLenRemaining )
                        
                        #Moves the iterator forward for each bit vector by the run length of me
                        me.moveIteratorForward(meLenRemaining)
                        you.moveIteratorForward(meLenRemaining)
                        
                    #If they are the same size or you is the longer run
                    else:
                                                
                        #Adds the AND'ed word to the new bitVector
                        new.appendRun( youType , youLenRemaining )
                        
                        #Moves the iterator forward for each bit vector by the run length of you
                        me.moveIteratorForward(youLenRemaining)
                        you.moveIteratorForward(youLenRemaining)
                        
                    
                #If only me is a run of 0's
                elif meType == 0:
                                                            
                    #Adds the run of 0's to the new bitVector
                    new.appendRun( meType , meLenRemaining )
                    
                    #Moves the iterator forward for each bit vector by the run length of me
                    me.moveIteratorForward(meLenRemaining)
                    you.moveIteratorForward(meLenRemaining)  
                    
                #If only you is a run of 0's
                elif youType == 0:
                                                            
                    #Adds the run of 0's to the new bitVector
                    new.appendRun( youType , youLenRemaining)
                    
                    #Moves the iterator forward for each bit vector by the run length of you
                    me.moveIteratorForward(youLenRemaining)
                    you.moveIteratorForward(youLenRemaining) 
                    
                #If both are runs of 1's
                else:
                                        
                    if meLenRemaining > youLenRemaining:
                        
                        #Adds the run of 1's to the new bitVector
                        new.appendRun( meType , youLenRemaining)
                        
                        #Moves the iterator forward for each bit vector by the run length of you
                        me.moveIteratorForward(youLenRemaining)
                        you.moveIteratorForward(youLenRemaining)
                        
                    #If they are the same size or you is the longer run
                    else:
                        
                        newWrd = meActiveWord
                        
                        #Adds the run of 1's to the new bitVector
                        new.appendRun( youType , meLenRemaining)
                        
                        #Moves the iterator forward for each bit vector by the run length of me
                        me.moveIteratorForward(meLenRemaining)
                        you.moveIteratorForward(meLenRemaining)
            #      
            #Case 3: One is literal and one is run
            #
            else:
        
                #If me is the run
                if (not meLiteral):
                                        
                    #Get the run type of me
                    meType = me.wahStorage.getRunType(meActiveWord)
                    
                    #If me is a run of 0's append the run of 0's and iterate by meLenRemaining
                    if meType == 0:
                                                
                        #Adds the run of 0's to the new bitVector
                        new.appendRun( meType , meLenRemaining)
                        
                        #Iterate both by the length of the run of 0's
                        me.moveIteratorForward(meLenRemaining)
                        you.moveIteratorForward(meLenRemaining)
                    
                    #Else me is a run of 1's and we should append the literal and iterate both by one word
                    else:
                        
                        newWrd = youActiveWord
                        
                        #Adds the AND'ed word to the new bitVector
                        new.appendWord(newWrd)
                        
                        #Iterate both to the next word
                        me.moveIteratorForward(1)
                        you.moveIteratorForward(1)
                    
                #If you is the run
                else:
                                                            
                    #Get the run type of you
                    youType = you.wahStorage.getRunType(youActiveWord)
                                    
                    #If you is a run of 0's append the run of 0's and iterate by meLenRemaining
                    if youType == 0:
                        #Adds the run of 0's to the new bitVector
                        new.appendRun( youType , youLenRemaining)
                        
                        #Iterate both by the length of the run of 0's
                        me.moveIteratorForward(youLenRemaining)
                        you.moveIteratorForward(youLenRemaining)
                        
                    
                    #Else you is a run of 1's and we should append the literal and iterate both by one word
                    else:
                                                
                        newWrd = meActiveWord
                        
                        #Adds the AND'ed word to the new bitVector
                        new.appendWord(newWrd)
                        
                        #Iterate both to the next word 
                        me.moveIteratorForward(1)
                        you.moveIteratorForward(1)
                        
        return bitVectorWAH(new)

if __name__ == "__main__":
    print "Running some testing code..."
    aNum = 0
    bNum = 0
    
    #Literal Word Test Vector a
    a = bitVectorWAH()
    a.append(1)
    for i in range(10):
        a.append(0)
    a.append(1)
    for i in range(12):
        a.append(0)
    a.append(1)
    
    #Literal Word Test Vector b
    b = bitVectorWAH()
    b.append(0)
    b.append(1)
    for i in range(7):
        b.append(0)
    b.append(1)
    for i in range(8):
        b.append(0)
    b.append(1)
    for i in range(5):
        b.append(0)
    b.append(1)
    
    
    # Adds runs to a and b
    for i in range(173):
        a.append(0)
    for i in range(42):
        a.append(1)
    for i in range(23):
        a.append(0)
    for i in range(25):
        a.append(1)
    for i in range(227):
        b.append(1)
    for i in range(35):
        b.append(0)
    b.append(1)

    
    print a
    print b
    '''
    ##Test operations##
    print a.XOR(b)
    print a.OR(b)
    print a.AND(b)
    '''
    
    '''
    ##Test COUNT##
    print b.COUNT()
    '''
