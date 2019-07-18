#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:48:52 2019

@author: admin
"""

import numpy as np
import pandas as pd
import sys
sys.path.append("../../bitmaps/WAH")
sys.path.append("../../bitmaps")

from ABCBitVector import ABCBitVector
from bitVectorWAH import bitVectorWAH

from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id, col
from Indexs import Indexs

class UpdateIndex(Indexs):
    
    # add on another row
    def appendRow( rowID, newVal):
        pass
    
    # remove an added row
    def deleteRow( rowID):
        pass
    
    #remove a row than add a row inplace of it
    def updateRow( rowID, newVal):
        pass