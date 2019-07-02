from pyroaring import BitMap
from ABCBitVector import ABCBitVector

class bitVectorRoaring(ABCBitVector):
    def __init__(self,roar = BitMap()):
        self.num_row = 0
        self.baseStorage = roar
        
    def AND(self,other):
       return bitVectorRoaring(self.roar & other)
    
    def XOR(self, other):
        return bitVectorRoaring(self.baseStorage.__xor__(other))
    
    def OR(self, other):
        return bitVectorRoaring(self.baseStorage.__or__(other))
    
    def append(self, bit):
        if( bit == 1 ):
            self.baseStorage.add(self.num_row)
            
        self.num_row += 1
        
if __name__ == "__main__":
    a = bitVectorRoaring()
    a.append(1)
    for i in range(10):
        a.append(0)
    a.append(1)
    print a