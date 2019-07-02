# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 10:26:35 2019

@author: swozniak
"""
from pyspark.sql import SparkSession

import numpy as np
import pandas as pd

#Initialize spark session
spark = SparkSession.builder.master("local").getOrCreate()
#Create easy variable for spark context
sc = spark.sparkContext
#Sample bitVectors
bv1_list = np.array([1, 2, 3, 4, 4, 3, 2, 1],dtype=np.uint64).tolist()
bv2_list = np.array([1, 2, 3, 4, 2, 1],dtype=np.uint64).tolist()
#Pandas dataframe of bitvectors and ids
bvs = pd.DataFrame([(0,bv1_list), (1,bv2_list)], columns=['IDs','Bit Vectors'])
#Spark dataframe of same things
sparkDataFrame = spark.createDataFrame(bvs)
#printing the dataframe
sparkDataFrame.show()