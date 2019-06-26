# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 10:46:46 2019

@author: josiah_mcclurg
"""

## An iterator which loops through a WAH storage array.
#  Also provides functions for fast forwarding.
class WAHStorageWordIterator(object):
    
    ## @var wordSizeInBits
    #  The number of bits in each word
    
    ## @var storage
    #  The compressed bitmap
    
    ## @var activeWordIndex
    #  The index of the current active word in this iterator.
    
    ## @var lenRemaining
    #  The number of words remaining in the active run. Does not include the
    #  Does not include the active word. Should be zero if the active word is
    #  a literal.
    
    ## Initializes an iterator starting at the beginning of storage
    def __init__(self, wahStorage):
        self.wahStorage = wahStorage
        self.activeWordIndex = 0
        self.wordsProcessed = 0
        
        self.activeWord = self.wahStorage.getWordAt(self.activeWordIndex)
        if self.wahStorage.isLiteral(self.activeWord):
            self.lenRemaining = self.wahStorage.dtype(0)
        else:
            self.lenRemaining = self.wahStorage.getRunLen(self.activeWord)
        
    def __iter__(self):
        return self
    
    ## Moves the iterator forward by one.
    def __next__(self):
        return self.moveIteratorForward(1)

    def next(self):
        return self.__next__()
    
    def current(self):
        return ((self.activeWord,self.lenRemaining))
    
    def isDone(self):
        return self.wordsProcessed >= self.wahStorage.getTotalLength()
    
    ## Moves the iterator forward by numWords
    #  @param numWords - The number of words to move.
    #  @return (new active word, length remaining) 
    def moveIteratorForward(self,numWords):
        if self.isDone():
            raise StopIteration
        
        else:         
            while(numWords > 0):
                # Because the length remaining does not include current word,
                # then lenRemaining == 0 means that we are finished with the current
                # run or literal, and are ready to move to the next one.
                if self.lenRemaining == self.wahStorage.dtype(0):
                    
                    # Move to the next word
                    self.activeWordIndex += 1
                    self.activeWord = self.wahStorage.getWordAt(self.activeWordIndex)
                    
                    # If new active word is a run, set length remaining accordingly. 
                    if not self.wahStorage.isLiteral( self.activeWord ):
                        self.lenRemaining = self.wahStorage.getRunLen(self.activeWord)
                        
                    # If new active word is a literal, set length to one
                    else:
                        self.lenRemaining = self.wahStorage.dtype(1)
                
                # You processed a word, so decrease the length remaining.
                self.lenRemaining -= self.wahStorage.dtype(1)
                numWords -= 1
                self.wordsProcessed += 1
                
            #print "Processed %d words..."%(self.wordsProcessed)
            return ((self.activeWord,self.lenRemaining))
    
if __name__ == "__main__":
    print "Running some testing code..."
    from WAHStorageWordBuilder import WAHStorageWordBuilder
    a = WAHStorageWordBuilder()
    a.appendRun(0,3)
    a.appendWord(0)
    a.appendRun(1,3)
    a.appendWord(33)
    print a
    
    b = iter(WAHStorageWordIterator(a))
    #print next(b)
    #print next(b)
    #print next(b)
    #print next(b)
    #print next(b)
    #print next(b)
    
    b = WAHStorageWordIterator(a)
    print b.moveIteratorForward(0)
    print b.moveIteratorForward(5)