# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:59:09 2019
@author: swozniak

This method collects unique elements and 
loops to map value to specified column.

Complete list of data Columns:
ID	Case Number	Date	Block	IUCR	Primary Type	Description	Location Description	Arrest	Domestic	Beat	District	Ward	Community Area	FBI Code	X Coordinate	Y Coordinate	Year	Updated On	Latitude	Longitude	Location	Historical Wards 2003-2015	Zip Codes	Community Areas	Census Tracts	Wards	Boundaries - ZIP Codes	Police Districts	Police Beats

"""

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


"""
# FIXME: Uncomment these!

#df.select("Primary Type").distinct().show()
df_primaryType = df.select("Primary Type").distinct()
values_primaryType = df_primaryType.collect()

#df.select("District").distinct().show()
df_district = df.select("District").distinct()
values_district = df_district.collect()


index_primaryType = []
print "\nIndex for Primary Type:\n"
for v in values_primaryType:
    print "Primary Type == %s (1st 10 values):"%(v[0])
    pt = df.select("Primary Type").rdd.map(lambda row: row[0] == v[0])
    index_primaryType.append(pt)
    print pt.take(10)


index_district = []
print "\nIndex for District:\n"
for v in values_district:    
    print "District == %s (1st 10 values):"%(v[0])
    d = df.select("District").rdd.map(lambda row: row[0] == v[0])
    index_district.append(d)
    print d.take(10)

#Creates and prints a binary index for 'Primary Type'
bin_primaryType = ''
temp_pt = pt.take(200)
for i in temp_pt:
    if i == False:
        bin_primaryType += '0'
    elif i == True:
        bin_primaryType += '1'
print bin_primaryType

#Creates and prints a binary index for 'District'
bin_district = ''
temp_d = d.take(200)
for i in temp_d:
    if i == False:
        bin_district += '0'
    elif i == True:
        bin_district += '1'
print bin_district
"""

# Make an ID column
dfWithID = df.withColumn("RowID",monotonically_increasing_id())

index_locationDescription = []
print "\nIndex for Location Description:\n"
for v in values_locationDescription:    
    print "Location Description == %s:"%(v[0])
    # Filter away anything that doesn't match this location description.
    # Note that we are also getting a RowID, which we can use to add the right row to the index
    rowIDs = dfWithID.select("RowID","Location Description").filter(col("Location Description") == v[0]).select("RowID").sort("RowID").collect()
    bv = bitVectorWAH()
    for row in rowIDs:
        #print row
        bv.add(row[0])
    
    index_locationDescription.append(bv)
    print bv
