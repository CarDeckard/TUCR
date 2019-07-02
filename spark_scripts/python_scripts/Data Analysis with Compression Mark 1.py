# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:59:09 2019
@author: swozniak

This method collects unique elements and 
loops to map value to specified column.

Complete list of data Columns:
ID	Case Number	Date	Block	IUCR	Primary Type	Description	Location Description	Arrest	Domestic	Beat	District	Ward	Community Area	FBI Code	X Coordinate	Y Coordinate	Year	Updated On	Latitude	Longitude	Location	Historical Wards 2003-2015	Zip Codes	Community Areas	Census Tracts	Wards	Boundaries - ZIP Codes	Police Districts	Police Beats

"""

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("test").getOrCreate()

df = spark.read.csv('Crimes -2001 to present (Sample).csv',header=True)


#df.select("Primary Type").distinct().show()
df_primaryType = df.select("Primary Type").distinct()
values_primaryType = df_primaryType.collect()

#df.select("District").distinct().show()
df_district = df.select("District").distinct()
values_district = df_district.collect()

#df.select("Location Description").distinct().show()
df_locationDescription = df.select("Location Description").distinct()
values_locationDescription = df_locationDescription.collect()


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

index_locationDescription = []
print "\nIndex for Location Description:\n"
for v in values_locationDescription:    
    print "Location Description == %s (1st 10 values):"%(v[0])
    ld = df.select("Location Description").rdd.map(lambda row: row[0] == v[0])
    index_locationDescription.append(ld)
    print ld.take(10)

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

#Creates and print a binary index for 'Location Description'
bin_locationDescription = ''
temp_ld = ld.take(200)
for i in temp_ld:
    if i == False:
        bin_locationDescription += '0'
    elif i == True:
        bin_locationDescription += '1'
print bin_locationDescription

"""
columns = ['ID\'s', 'BitVectors']
values = [('Primary Type', bin_primaryType)]


bitVector_rdd = sc.parallelize(List(line)).collect()
bitVector_df = spark.createDataFrame(columns, values)    
   # df_locationDescription.show()
"""