#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:48:17 2019

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

class Indexs(object):
    #returns row that was asked for
    def readRow(bitMap, row):
        pass
    
    #returns column that was asked for
    def readCol(bitMap, col):
        pass
    