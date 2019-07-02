from abc import ABCMeta, abstractmethod

class ABCBitVector(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, baseStorage):
        self.baseStorage = baseStorage
        
    @abstractmethod    
    def AND(self, other):
        pass
    
    @abstractmethod
    def XOR(self, other):
        pass
    
    @abstractmethod
    def OR(self, other):
        pass
    
    @abstractmethod
    def append(self, bit):
        pass
    
    def __str__(self):
        return str(self.baseStorage)
        
        
    
    