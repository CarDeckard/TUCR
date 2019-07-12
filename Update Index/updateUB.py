#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:50:08 2019

@author: admin
"""

import numpy as np
import pandas as pd
import sys
sys.path.append("../../bitmaps/WAH")
sys.path.append("../../bitmaps")

from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id, col

class updateUB():
    
    ###################################################
    #     UPBM      ##    bitMap     ##UPBM XOR bitMap#
    ###################################################
    # 0   1   0   1 ## 0   1   0   0 ## 0   0   0   1 #
    # 0   0   0   0 ## 1   0   0   0 ## 1   0   0   0 #
    # 1   0   0   1 ## 0   0   0   1 ## 1   0   0   0 #
    # 0   0   0   0 ## 0   0   1   0 ## 0   0   1   0 #
    ###################################################
    
    def __init__(bitMap):
        numRows = bitMap.count
        numCols = len(bitMap.columns)
        
        #create an array of empty vectors matching the size of bitMap
    
    def readRow(rowID):
        #returns the XOR of the row from the original BM and the UpBit BM
        
    def readCol(colID):
        #returns the XOR of the column from the original BM and the UpBit BM

    def updateRow( bitMap, rowID, newVal):
        #searches through the original BM and finds where the set bit is
        #for the given rowID. That is than also set in the same location in 
        #the UpBit BM.Than set the bit at newVal x rowID.