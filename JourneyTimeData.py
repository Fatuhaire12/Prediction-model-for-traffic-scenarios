#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 14:46:51 2023

@author: fatumah
"""
#We need to install some packages first 
# For webscrapping using selenium
from selenium import webdriver #web browser testing, extract information from websites
from selenium.webdriver.chrome.service import Service #
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from parsel import Selector

# To delay as the website loads
from time import sleep

# For data manipulation
import pandas as pd
import numpy as np

# To download the files from the internet
import requests

# To automate opening a new window
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

# open the National Highways website
driver.get('http://tris.highwaysengland.co.uk/detail/journeytimedata')


#grab the html
sel = Selector(text = driver.page_source)

# locate the Motorway button; in this case M6 Toll (because it had few zip files). 
#Replace m6toll with m3 for M3 motorway
motorway_button = driver.find_element("xpath",'//*[@id="site-heading-m3"]/h4/a')

# click it
motorway_button.click()


# Wait for a few seconds for the page to load before
sleep(15)

# locate the year button; in this case 2023. Replace m6toll with m3 for M3 motorway
year_button = driver.find_element("xpath",'//*[@id="site-collapse-m3"]/div/div[9]/button')

#selet the html
sel = Selector(text = driver.page_source)

# Grab all the links for the various zip files. Replace M6-TOLL with M3 for M3 motorway
data_links = sel.xpath('//*[@id="M3+2023"]/table[1]/tbody/tr/td/a/@href').getall()
data_links


# Grab all the names for the various zip files
data_names = sel.xpath('//*[@id="M3+2023"]/table[1]/tbody/tr/td/a/text()').getall()
data_names


# Pull down the zip files into a folder on our local machine. We keep them as zip files to save space
# To comment out after initial use
for i in range(len(data_links)):
    url = 'http://tris.highwaysengland.co.uk'+data_links[i]
    response = requests.get(url)
    
    file_name = data_names[i]
    with open(file_name, 'wb') as f:
        f.write(response.content)
        
# Initialize an empty dataframes to combine the different zip files
# We stick to the file meta data for now to focus on the GPS Ref info
file_meta_data = pd.DataFrame(columns=['MIDAS ID','Legacy MIDAS ID','Site Name'])
#file_meta_data = pd.DataFrame(columns=['NTIS Link Description','Start Node Coordinates',
#                                       'End Node Coordinates','Link Length'])
#speed_data = pd.DataFrame(columns=['Local Date', 'Local Time', 'Total Carriageway Flow',
#                                   'Total Flow vehicles less than 5.2m','Total Flow vehicles 5.21m - 6.6m',
#                                   'Total Flow vehicles 6.61m - 11.6m','Total Flow vehicles above 11.6m',
#                                   'Speed Value','Quality Index','Network Link Id','NTIS Model Version'])
   
#Column names for journey time data   
#file_meta_data = pd.DataFrame(columns= ['Local Date','Local Time','Day Type ID','NTIS Link Number','Road','Carriageway',                                          
# 'NTIS Link Description', 'NTIS Model Version','Link Length','Start Node Coordinates','End Node Coordinates',
# 'Total Traffic Flow','Profile Traffic Flow','Traffic Flow %value1', 'Traffic Flow %value2', 'Traffic Flow %value3','Traffic Flow %value4',                                          
# 'Flow Quality','Fused Travel Time', 'Profile Travel Time', 'Fused Average Speed', 'Quality Index'])                                                
#    
#################    

# We read in the zip files saved to our machine from above and concatenate data from different files

for i in range(len(data_names)):
    file_name  = data_names[i]
    # The first three rows include the file meta-data
    file_meta_data2= pd.read_csv(file_name, error_bad_lines=False)
#    file_meta_data2.columns= ['Local Date','Local Time','Day Type ID','NTIS Link Number','Road','Carriageway',                                          
# 'NTIS Link Description', 'NTIS Model Version','Link Length','Start Node Coordinates','End Node Coordinates',
# 'Total Traffic Flow','Profile Traffic Flow','Traffic Flow %value1', 'Traffic Flow %value2', 'Traffic Flow %value3','Traffic Flow %value4',                                          
# 'Flow Quality','Fused Travel Time', 'Profile Travel Time', 'Fused Average Speed', 'Quality Index']
    file_meta_data = file_meta_data.append(file_meta_data)
    # The rest of the file includes the numbers and columns of interest
 #   speed_data = pd.read_csv('file.zip', compression='zip', skiprows=3, 
  #                           dtype={'Total Carriageway Flow': int, 'Total Flow vehicles less than 5.2m': int, 
  #                                  'Total Flow vehicles 5.21m - 6.6m': float})        
  
# Write the concatenated data to a csv file on the current directory on our machine 
file_meta_data.to_csv('M3_GPS_data.csv', index = False)


# Node table.






     