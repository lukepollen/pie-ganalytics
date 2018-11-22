# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 17:16:43 2018

@author: Cortica
"""

# Update period comparison to state time comparison
from displayfunctions import month_compare, period_compare
from plotfunctions import makeBarPlot, makeLinePlot, dataFrameXTicks
from dataFrameFunctions import groupByDescending, dataFrameSlice, dateSliceGeneration, initializeDataFrame, monthRangeGeneration
import operator
import pandas as pd
import numpy as np

# Groups the data in a column. Charts relative percentage of items belonging to category defined by np.where().    
def conditionalStackedBar(targetColumn, conditions, groupColumn):
    
    # Create a series which describes whether the dataFrame row is in some condition.
    # Compares the column values in sourceData[targetColumn] with the operator (conditions[0]) to an amount (conditions[1])
    sourceVolume = np.where(getTruth(sourceData[targetColumn], conditions[0], conditions[1]), conditions[2], conditions[3])
    # Group by the targetColumn and give the number of respective conditions for that entity.
    bySourceVolume = sourceData.groupby([groupColumn, sourceVolume])
    # Unstack into a table.
    aggCounts = bySourceVolume.size().unstack().fillna(0)
    # Use an indexer to sort in ascending order
    indexer = aggCounts.sum(1).argsort()
    # Select rows in order and take the last ten rows.
    countSubset = aggCounts.take(indexer)[-10:]
    # Print cand chart the countSubset
    print(countSubset)
    countSubset.plot(kind='barh', stacked=True)
    # Normalised plot. Shows proportion of entities relative to 1.
    normedSubset = countSubset.div(countSubset.sum(1), axis=0)
    normedSubset.plot(kind='barh', stacked=True)
    
# Prints all the data in the dataframe to the iPython console.
def print_full(x):
    
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')
    
# Returns a boolean given two inputs and an operator.
def getTruth(inp, relate, cut):
    
    ops = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '=': operator.eq}
    return ops[relate](inp, cut)

    #print getTruth(1.0, '>', 0.0)  # prints True
    #print getTruth(1.0, '<', 0.0)  # prints False
    #print getTruth(1.0, '>=', 0.0)  # prints True
    #print getTruth(1.0, '<=', 0.0)  # prints False
    #print getTruth(1.0, '=', 0.0)  # prints False

# Converts a column to float
def getFloats(dataFrame, targetColumn):
    
    # Ensure that type is correctly cast to float to avoid integer floor division
    floats = dataFrame[targetColumn].astype(float)
    dataFrame[targetColumn] = floats

# Show groupby a column and then show the total and mean aggregates for these values based on another column.
def groupAggregate(groupColumn, targetColumn, aggType):
    
    grouped = sourceData.groupby([groupColumn])
    groupedValue = grouped[targetColumn]
    bySource = groupedValue.agg(aggType).sort_values(ascending=False)
    # Ensures labels correctly match their associated values.
    bySource.sort_index(ascending=False)
    # Create chart and give dataFrame data for total.
    print('\n' + aggType + " " + targetColumn + " by " + groupColumn)    
    bySource[:10].plot(kind='barh', rot=0)

### Default Variables
sizeList = [12, 6]    
    
### Data Load
sourceData = initializeDataFrame("_keywords", "2017-10-21", ['medium', 'source', 'country', 'region', 'keyword', 'socialnetwork', 'sessions', 'avgsessionduration', 'pageviews', 'bouncerate', 'pageviewspersession', 'transactionrevenue', 'origin'])
adsenseData = initializeDataFrame("_adsense", "2017-10-21", ['country', 'metro', 'devicecategory', 'medium', 'source', 'year',  'month', 'sessions', 'adsenseecpm', 'adsenserevenue', 'origin'])

# Chart the top ten session providers and chart whether the relative percentage of high volume visits from the source.
groupAggregate('source', 'sessions', 'sum')
groupAggregate('source', 'sessions', 'mean')  
conditionalStackedBar('pageviews', ['>', 5, 'High Volume', 'Low Volume'], 'source')

### Creating a pivot table based on country and regions for countries with more than 100 sessions. 
# Ultimately sort the country-region combination on search engine traffic.
meanSource = pd.pivot_table(sourceData, values='sessions', index=['country', 'region'], columns='medium', fill_value=0, aggfunc=np.sum)
meanSource.sortlevel(['country', 'region'], ascending=[False, False], sort_remaining=False)
print(meanSource)
# Get countries with regular occurences of sessions
sessionsByCountry = sourceData.groupby('country').size()
# Sort so that the most active country comes first.
sessionsByCountry = sessionsByCountry.sort_values(ascending=False)
# Get countries whose channel data has been seen at least 100 times. 
activeCountries = sessionsByCountry.index[sessionsByCountry >= 100]
# Slice the original pivot table down to only active countries.
meanSourceActive = meanSource.ix[activeCountries]
print(meanSourceActive)
# Sort by the top organic country-region combinations.
topOrganicRatings = meanSourceActive.sort_index(by='organic', ascending=False)
print(topOrganicRatings) 

### Compare the difference between organic and direct traffic for country-region sources.
meanSourceActive['organicDirectDiff'] = meanSourceActive['organic'] - meanSourceActive['(none)']
sortedByDifference = meanSourceActive.sort_index(by='organicDirectDiff')
# Prints the greatest negative twenty (more direct than organic) and then greatest positive (more organic than direct).
sortedByDifference[:20]
sortedByDifference[::-1][:20]
# Standard deviation of sessions grouped by country   

### Get the standard deviation of each active country for session sources and sort by the countries with greatest difference.
sessionStdByCountry = sourceData.groupby('country')['sessions'].std()
sessionStdByCountry = sessionStdByCountry.ix[activeCountries]
sessionStdByCountry.sort_values(ascending=False)

# Print series of session sources for each country
sourceData.groupby('country')['sessions'].sum().sort_values(ascending=False)
# Repeat for regions.
sourceData.groupby(['country', 'region'])['sessions'].sum().sort_values(ascending=False)

# Create a plot of the sources from a pandas pivot table.
sourcesOverTime = pd.pivot_table(sourceData, values='sessions', index='origin', columns='medium', aggfunc=np.sum)
sourcesOverTime.plot(title='Traffic this year', figsize=(12, 6))

# For each day and medium column, extract the top 1000 pageview providers.
pieces = []
for origin, medium in sourceData.groupby(['origin', 'medium']):
    pieces.append(medium.sort_index(by='pageviews', ascending=False)[:1000])
top1000 = pd.concat(pieces, ignore_index=True)    

# Creating segments of the top performers.
organic = top1000[top1000.medium == 'organic']
referral = top1000[top1000.medium == 'referral']

# Plotting overal performance, concentrating on the aggregates from the top performers.
topPerformers = pd.pivot_table(top1000, values='pageviews', index='origin', columns='medium', aggfunc=np.sum)
topPerformers
topPerformers.plot(title='Traffic this year', figsize=(12, 6))
