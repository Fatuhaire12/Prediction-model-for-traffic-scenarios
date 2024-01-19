#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 18:13:06 2023

@author: fatumah
"""

#Create node table
import pandas as pd

# Specify the file path
file_path = '/home/fatumah/Dropbox/R_codes/M3 westbound within J4A mainCarriageway 103050402.csv'
#(file ='M3 westbound within J4A mainCarriageway 103050402.csv',header= TRUE)

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)
#check
df.head
#get column names here
column_names = df.columns 
# Extract specific columns by their names

NodeTable = df.iloc[:1, [6, 9, 10]]
#for more than one datasets, create a for loop that can read multiple csv files and extract
# "NTIS Link Description", "Start Node Coordinates", "End Node Coordinates". 
#The NodeTable is just for 1 scv file.



