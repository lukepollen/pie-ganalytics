# -*- coding: utf-8 -*-
"""
Created on Mon Jan 04 14:00:02 2016

@author: Anima
"""

# Add machine learning for general classifcation of keyword data.
# Report by country and report with classified top keywords 

import pandas as pd
from dataFrameFunctions import initializeDataFrame, dateSliceGeneration, dataFrameSlice, groupByDescending, rankedDictionary

data = initializeDataFrame("_keywords", "2017-06-01", ['medium', 'source', 'country', 'region', 'keyword', 'socialnetwork', 'sessions', 'avgsessionduration', 'pageviews', 'bouncerate', 'pageviewspersession', 'transactionrevenue', 'origin'])
        
ym_key_pairs = dateSliceGeneration()
currentYear = str(ym_key_pairs[len(ym_key_pairs) -1][1])
### Charting Data

all_keywords = data.groupby('keyword')['sessions'].sum()
all_keywords.sort_values(ascending=False, inplace=True, kind='quicksort', na_position='last')
print('\n' + 'All Keywords')
print(all_keywords)

# print full_year

#last_year_keywords = data[data['year'] == currentYear]
last_year_keywords = dataFrameSlice(data, {currentYear : "origin"})
full_year = last_year_keywords.groupby('keyword')['sessions'].sum()
full_year.sort_values(ascending=False, inplace=True, kind='quicksort', na_position='last')
print('\n' + 'Full Year')
print(full_year)

# Generic keyword data for last month and last 12 full months
#last_month_keywords = data[(data['month'] == ym_key_pairs[11][0]) & (data['year'] == ym_key_pairs[11][1])]
last_month_keywords = dataFrameSlice(data, {ym_key_pairs[11][0] : "origin", ym_key_pairs[11][1] : "origin"})
value = last_month_keywords.groupby('keyword')['sessions'].sum()
value.sort_values(ascending=False, inplace=True, kind='quicksort', na_position='last')
print('\n' + 'Last Month')
print(value)

# print keywords greater_than_fifty

greater_than_fifty = pd.DataFrame(full_year, columns=['sessions'])
greater_than_fifty = greater_than_fifty[greater_than_fifty.sessions >= 50]
print('\n' + 'Greater Than Fifty')
print(greater_than_fifty)

# Printing the top countries by medium and sources for organic. 

organic = dataFrameSlice(data, {ym_key_pairs[11][1] : "origin"}, {"medium" : "organic"})
organicDescending = groupByDescending(organic, ['country', 'sessions'], 6)
print('\n' + 'By Country, Current Year:')
print(organicDescending)

#organic = dataFrameSlice(data, {}, {"source" : "google"})
#organicDescendingGoogle = groupByDescending(organic, ['country', 'sessions'], 6)
#print(organicDescendingGoogle)

# Keywords in aggregate for top six countries
# Uses the rankedDictionary function to convert the organicDescending dataFrame to a dictionary.
country_sort = rankedDictionary(6, organicDescending)

for key in country_sort.keys():
    print('\n' + key)    
    isolate_keywords = data.loc[(data['country'] == key) & (data['keyword'] != '(not provided)') & (data['keyword'] != '(not set)') & (data['medium'] == 'organic')]
    print(groupByDescending(isolate_keywords, ['keyword', 'sessions'], 1))