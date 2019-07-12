#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 10:52:01 2019

@author: admin
"""

from ABCBitVector import ABCBitVector
from bitVectorWAH import bitVectorWAH


'''
    In-Place Update acts by unsetting 'A' and than setting 'B' in the matching 
    location casuing the value at that location to change. 
    
    @param self         - bit vector that is being unset
    @param other        - bit vector that is being set 
    @param updateMask   - mask of the location that is being changed 

'''
def InPlaceUpdate(self, other, updateMask):
    
    #updateMask holds the location that is being update we can AND
    #self with the flip of updateMask to copy over everything but that one bit
    self.baseStorage.storage = self.AND( ~(updateMask) )
    
    #doing an OR with other and updateMask changes the location of the update 
    other.baseStorage.storage = other.OR(updateMask)
    
    
    
'''
    UpBit relies on a second bitmap to keep track of what needs to be updated 
    with the main bitmap. In order to update correctly the row and column that
    is going to be set needs to be supplied. This is so the updateBM can mark
    what locations are going to be flipped when an XOR is opperated
    
    @param originalBM   - original bitmap 
    @param updateBM     - bitmap keeping track of updates
    @param rowID        - row in which the update is to take place
    @param column       - column in which the update is to be set
    
'''
def UpBit(originalBM, updateBM, rowID, column):
    '''
    
    1) Find where the set bit is in the rowID
    
    2) set location of the set bit in updateBM 
    
    3) set location of the RowXColumn in updateBM
    

    if roaringBM:
        
        
    elif WAH:
        
    '''
    
    
    
'''
    Change the original bitmap to reflect the changes that have accumulated in
    the update bitmap 
'''
    
def pushUpBit(originalBM, updateBM):
    
    originalBM ^= updateBM
    
    
'''
    Update Conscious Bitmap works by storing a dirty bit to represent if the
    row is valid or not. When updating the row dirty bit is unset. The row is
    than added at the bottom of the bitmap keeping the rowID and setting the
    dirty bit 
    
    @param originalBM   - original bitmap to be updated
    @param rowID        - row ID vector
    @param EV           - dirty bit vector 
'''
    
def UCB(originalBM, rowID, EV):
    
    
    