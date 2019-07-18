#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:49:38 2019

@author: admin
"""

import numpy as np
import pandas as pd
import sys
sys.path.append("../UpdateIndex")
sys.path.append("../UpdateIndex")

from ABCBitVector import ABCBitVector
from bitVectorWAH import bitVectorWAH

from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id, col

class updateUCB():
    
    ##############################
    # EV ##    bitMap     ## RID #
    ##############################
    # 1  ## 0   1   0   0 ##  0  #
    # 0  ## 1   0   0   0 ##  1  #
    # 0  ## 0   0   1   0 ##  2  #
    # 1  ## 0   0   0   1 ##  3  #
    ##############################
    #AOEV##     AOBM      ##AORID#
    ##############################
    # 1  ## 0   0   1   0 ##  1  #
    # 1  ## 1   0   0   0 ##  2  #
    ##############################
    
    def __init__(bitMap, ):
        #create a seperate EV vector that is all 1's for the length of bitMap rows
        #create an addOnEV vector that will match the added on bitmap
        #create an addOnBM for the appended rows to be added to
        #create an addOnRowID for the appended rowIDs to be added to

    def readRow(bitMap, rowID):
        #finds where the EV for the given rowID is set, returns row
        
    def readCol(bitMap, colID):
        #if EV is unset skip this row, if set row value is appended to
        #a vector, vector is than returned 
        
    def appendRow( rowID, newValue):
        #append a new row to the added bitmap, set the EV, set the rowID 
        #to be the maxRow + 1
        
    def deleteRow( rowID):
        #unset the EV of the given rowID
        
    def updateRow( rowID, newValue):
        #deleteRow and than appendRow