# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:59:09 2019
@author: swozniak

This method pairs each value with a row ID, distributes the 
load, and then combines the bitmap using a sorting agorithm 
to correct any out-of-order elements.

Complete list of data Columns:
ID	Case Number	Date	Block	IUCR	Primary Type	Description	Location Description	Arrest	Domestic	Beat	District	Ward	Community Area	FBI Code	X Coordinate	Y Coordinate	Year	Updated On	Latitude	Longitude	Location	Historical Wards 2003-2015	Zip Codes	Community Areas	Census Tracts	Wards	Boundaries - ZIP Codes	Police Districts	Police Beats

"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id
spark = SparkSession.builder.appName("test").getOrCreate()

df = spark.read.csv('Crimes -2001 to present (Sample).csv',header=True)

#df.select("Primary Type").withColumn("1").distinct().show()
df_primaryType = df.select("Primary Type").withColumn("RowID",monotonically_increasing_id())

# Make multiple partitions, to emulate multiple computers
a = df_primaryType.repartitionByRange(4,"RowID").orderBy("RowID")




#df.select("Primary Type").withColumn("RowID",monotonically_increasing_id()).show()
#index = []
#for v in values:
#    print "Index for Primary Type == %s (1st 10 values):"%(v[0])
#    i = df.select("Primary Type").rdd.map(lambda row: row[0] == v[0])
#    index.append(i)
#    print i.take(10)