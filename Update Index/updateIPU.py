#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:51:51 2019

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

class updateIPU(UpdateIndex):
    
    def __init__():
    
    def readRow(rowID):
        
        
    def readCol(colID):
        
    def appendRow( rowID, newValue):
        
    def deleteRow( rowID):
        
    def updateRow( rowID, newValue):
        
    