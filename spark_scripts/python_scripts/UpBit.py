# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 14:14:45 2019

@author: clehrian
"""
##########################################################################
############################## UpBit #####################################
##########################################################################

import sys
sys.path.append("../../bitmaps/WAH")
sys.path.append("../../bitmaps")

import numpy as np
import csv

from ABCBitVector import ABCBitVector
from bitVectorWAH import bitVectorWAH


from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("UpBit").getOrCreate()

df = spark.read.csv('Crimes -2001 to present (Sample).csv',header=True)

#df.select("Location Description").distinct().show()
df_locationDescription = df.select("Location Description").distinct()
values_locationDescription = df_locationDescription.collect()

#Get update tuples in
def readInData(dataFile):
    with open(dataFile,"r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        listOfLines = []
        for row in csv_reader:
            updateRow = row["UpdateRow"]
            locationDescription = row["LocationDescriptionPosition"]
            dataTuple = tuple((updateRow,locationDescription))
            listOfLines.append(dataTuple)
    return listOfLines

dataLines = readInData("E:\\TUCR\\spark_scripts\\python_scripts\\index_updates.csv")
print dataLines
#Create matrix to store data
updateMatrix = np.zeros((len(values_locationDescription),200),dtype=int)
print updateMatrix

for i,j in dataLines:
    updateRow = int(i)
    locationDescription = int(j)
    print updateRow
    print locationDescription

#Read in bitmap to update
bitmap = spark.read.parquet("test9.parquet")
#bitmap.show()
#Convert storage to BitVector class

#Gets only the bitvector column
bitmapWithOnlyBitVectors = bitmap.select('BitVectors')
#bitmapWithOnlyBitVectors.show()
listOfRowObjects = bitmapWithOnlyBitVectors.collect()
#Makes list of bitVector Objects
bitVectors = []
for i in range(len(listOfRowObjects)):
    storage = listOfRowObjects[i][0]
    bv = bitVectorWAH()
    for i in storage:
        bv.appendWord(i)
    bitVectors.append(bv)
print bitVectors[0]
print bitVectors[1]

def findPositionForUpdate(positionInDataLines): #Will be number
    updateRow = int(dataLines[positionInDataLines][0])
    print updateRow
    searcher = bitVectorWAH()
    for j in range(bitVectors[positionInDataLines].baseStorage.numRows):
        if j == updateRow:
            searcher.append(1)
        else:
            searcher.append(0)
    print searcher.baseStorage.storage
    return searcher, updateRow
final = []
for i in range(len(dataLines)):
    pos,updateRow = findPositionForUpdate(i)
    print pos
    print updateRow
    res = []
    res1 = []
    for j in range(len(bitVectors)):
        a = bitVectors[j].AND(pos)
        appendTuple = (updateRow,a)
        res.append(appendTuple)
        
        for bitVectorID in range(len(res)):
            for index in range(4):
                try:    
                    if (res[bitVectorID][1].baseStorage.getWordAt(index) != np.int64(0)) and ((res[bitVectorID][1].baseStorage.getWordAt(index) & (np.int64(1) << np.int64(63))) == np.int64(0)):
                        if len(res1) >= 1:
                            pass
                        else:
                            appendTuple = (bitVectorID,updateRow)
                            final.append(appendTuple)
                            res1.append(appendTuple)
                        
                    else:
                        pass
                except IndexError:
                    pass

print final
#Finally time to add updates to the matrix and xor the two together
#for i,j in final:
    
        
      
        