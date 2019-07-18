# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:59:09 2019
@author: clehrian & swozniak

This method collects unique elements and 
loops to map value to specified column.

Complete list of data Columns:
ID	Case Number	Date	Block	IUCR	Primary Type	Description	Location Description	Arrest	Domestic	Beat	District	Ward	Community Area	FBI Code	X Coordinate	Y Coordinate	Year	Updated On	Latitude	Longitude	Location	Historical Wards 2003-2015	Zip Codes	Community Areas	Census Tracts	Wards	Boundaries - ZIP Codes	Police Districts	Police Beats

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

spark = SparkSession.builder.appName("test").getOrCreate()

df = spark.read.csv('Crimes -2001 to present (Sample).csv',header=True)

#df.select("Location Description").distinct().show()
df_locationDescription = df.select("Location Description").distinct()
values_locationDescription = df_locationDescription.collect()

# Make an ID column
dfWithID = df.withColumn("RowID",monotonically_increasing_id())


index_locationDescription = []
print "\nIndex for Location Description:\n"
maxRowID = 0
for v in values_locationDescription:    
    print "Location Description == %s:"%(v[0])
    # Filter away anything that doesn't match this location description.
    # Note that we are also getting a RowID, which we can use to add the right row to the index
    rowIDs = dfWithID.select("RowID","Location Description").filter(col("Location Description") == v[0]).select("RowID").sort("RowID").collect()
    bv = bitVectorWAH()
    for row in rowIDs:
        #print row
        if row[0] > maxRowID:
            maxRowID = row[0]
        bv.add(row[0])
        
    
    index_locationDescription.append(bv)
    print bv.baseStorage.storage.tolist()
    
for bv in index_locationDescription:
    if((bv.baseStorage.numRows-1) < maxRowID):
        bv.add(maxRowID,0)

    
    
#Initialize spark session
#spark = SparkSession.builder.master("local").getOrCreate()
#Create easy variable for spark context
sc = spark.sparkContext

#Pandas dataframe of bitvectors and ids
tmp = [bv.baseStorage.storage.astype(np.int64,casting="unsafe").tolist() for bv in index_locationDescription]
tmp = zip([str(loc[0]).replace(" ", "_") for loc in values_locationDescription], tmp)
bvs = pd.DataFrame(data=tmp, columns=['LocationType','BitVectors'])
#Spark dataframe of same things
sparkDataFrame = spark.createDataFrame(bvs)
#printing the dataframe
sparkDataFrame.show()
sparkDataFrame.printSchema()
#make parquet file
sparkDataFrame.write.parquet("test9.parquet")


'''
#################################################################
#Let's go BACKWARDS BABY!!!                                     #
#################################################################
#Creates a variable for that parquet boi

parquetFile = spark.read.load("test8.parquet")

#Creates a name for this table.
parquetFile.createOrReplaceTempView("parquetFile")

temp = parquetFile
temp.sort("RowID").show()'''
