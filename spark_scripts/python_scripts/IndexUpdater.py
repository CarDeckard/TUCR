"""
Spyder Editor
Author: swozniak
Date: 07/16/19

"""

from os import path
import csv

def appendUpdate(updateRow, changeTo):
    with open('index_updates.csv', 'a+', buffering = 0) as csvfile:
        updateWriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        updateWriter.writerow([updateRow, changeTo])
    
if not(path.exists("index_updates.csv")):
    print("File 'index_updates.csv' does not exist, creating file now")
    with open('index_updates.csv', 'a+', buffering = 0) as csvfile:
        updateWriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        appendUpdate('UpdateRow', 'LocationDescriptionPosition')

appendUpdate(1,2)
appendUpdate(3,4)
appendUpdate(5,6)
