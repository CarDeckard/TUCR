from abc import ABC, abstractmethod

class ABCBitVector(ABC):
    
    @ABC.abstractmethod    
    def AND(self, other):
        pass
    
    def XOR(self, other):
        pass
    
    def OR(self, other):
        pass
    
    def append(self, other):
        pass
        
        
    
    