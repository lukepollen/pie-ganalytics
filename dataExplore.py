# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 14:38:58 2018

@author: Cortica
"""
import pandas as pd
from pandas import DataFrame
from dataFrameFunctions import initializeDataFrame
from pylab import *
import matplotlib.pyplot as plot

# Get the data and convert the 'origin column to a time series'
data = initializeDataFrame("the_source", "2013-06-11", ['medium', 'source', 'socialnetwork', 'sessions', 'avgsessionduration', 'pageviews', 'bouncerate', 'pageviewspersession', 'origin'])
data['origin'] = pd.to_datetime(data['origin'], errors='coerce')
#print(data)

#Get data for a single month. 
lastMonth = data.loc[(data['origin'].dt.year == 2018) & (data['origin'].dt.month == 5)]

# Does a count of the total rows.
print("Total session rows: " + str(lastMonth['sessions'].count()))

# Gives the total.
print("Total number of sessions: " + str(lastMonth['sessions'].cumsum().iloc[-1])) # Without the iloc[-1] the whole culumative sum data frame is returned.

# Organic sessions in the last month.
#lastMonthOrganic = lastMonth[lastMonth['medium'] == 'organic']
#print(lastMonthOrganic['sessions'].cumsum())

# Draq QQ plots of the main data.
array = data.iloc[:,5:10].values
plot.figure(figsize=(20,10))
plot.boxplot(array)
plot.xticks([1, 2, 3, 4, 5], ['sessions', 'avgsessionduration', 'pageviews', 'bouncerate', 'pageviewspersession'])
plot.xlabel(("Attribute Index"))
plot.ylabel(("Quartile Ranges"))
show()