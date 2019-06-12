# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pyspark

# Declare default variables for running the tutorials.
sc = pyspark.SparkContext.getOrCreate()
spark = pyspark.sql.SparkSession(sc)