from abc import ABC, astractmethod

class ABCBitVector(ABC):
    @abc.abstractmethod    
    def AND(self, other):
        pass
    
    def XOR(self, other):
        pass
    
    def OR(self, other):
        pass
    
    def appendWord(self, other):
        pass
        
        
    
    