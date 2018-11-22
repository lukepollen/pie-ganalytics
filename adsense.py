# -*- coding: utf-8 -*-
"""
Created on Mon Jan 04 13:50:14 2016

@author: Anima
"""

# Investigate difference in text vs chart print out for country + medium segmentation

import pandas as pd
from plotfunctions import makeBarPlot, makeLinePlot, revenueByMedium
from dataFrameFunctions import groupByDescending, dataFrameSlice, dateSliceGeneration, initializeDataFrame, monthRangeGeneration, rankedDictionary

### Global Values
sizeList = [12, 6]

# Loading the dataFrames
data = initializeDataFrame("the_source", "2017-06-01", ['medium', 'source', 'keyword', 'socialnetwork', 'sessions', 'avgsessionduration', 'pageviews', 'bouncerate', 'pageviewspersession', 'origin'])
adsense = initializeDataFrame("_adsense", "2017-06-01", ['country', 'metro', 'devicecategory', 'medium', 'source', 'socialnetwork', 'sessions', 'adsenseecpm', 'adsenserevenue', 'origin'])
ym_key_pairs = dateSliceGeneration()

# Months dictionary and container for dynamic generation of plot labels.
actual_months = monthRangeGeneration()

# Values for the devices
mobile_value = []
tablet_value = []
desktop_value = []

# Sums the values in slices of the main dataframe for each month / year combination.
for k, v in ym_key_pairs:
    mobile = dataFrameSlice(adsense, {k : "origin", str(v) : "origin"}, {"devicecategory" : "mobile"})    
    desktop = dataFrameSlice(adsense, {k : "origin", str(v) : "origin"}, {"devicecategory" : "desktop"})
    tablet = dataFrameSlice(adsense, {k : "origin", str(v) : "origin"}, {"devicecategory" : "tablet"})
    mobile_val = mobile['adsenserevenue'].sum()
    desktop_val = desktop['adsenserevenue'].sum()
    tablet_val = tablet['adsenserevenue'].sum()    
    mobile_value.append(mobile_val)
    tablet_value.append(tablet_val)
    desktop_value.append(desktop_val)

# Creating a dictionary used in makeLinePlot. Dictionary values are a list of monthly earnings for each device type (used as dictionary key)
valueDictionary = {
"Mobile" : mobile_value,
"Desktop" : desktop_value,
"Tablet" : tablet_value                   
}
makeLinePlot(sizeList, valueDictionary, actual_months, "Adsense by Device Category - Annual", 'Months', 'Adsense Earnings by Device')

avg_adsense_visitor = {}
country_list = []
country_total = []
user_adrevenue_value = []

# Getting count of the top five countried by sessions
top_five = groupByDescending(adsense, ['country', 'sessions'], 5)
# Assigning top five to dictionary
country_sort = rankedDictionary(5, top_five)

# Updating containers and plotting value by country.
for key in country_sort.keys():
    print('\n' + key)
    country_list.append(key)
    # Summing revenues for the current year    
    #country_currentYear = adsense[(adsense['year'] == ym_key_pairs[11][1]) & (adsense['country'] == key)]
    country_currentYear = dataFrameSlice(adsense, {ym_key_pairs[11][1] : "origin"}, {"country" : key})
    revenue_currentYear = country_currentYear['adsenserevenue'].sum()
    total_adsense = round(revenue_currentYear, 2)
    country_total.append(total_adsense)
    print('$' + str(total_adsense))    
    # Updating lists to plot the user average value.
    total_visits = country_sort[key]
    avg_visitor_value = total_adsense / total_visits
    user_adrevenue_value.append(avg_visitor_value)
makeBarPlot(sizeList, country_total, country_list, "Total Country Value", "Countries", "Total Revenue in $")    

# Charting on average user value and on country.
makeBarPlot(sizeList, user_adrevenue_value, country_list, "Adsense User Value", "Countries", "Average Value")    

#Container for Bar Plot
adsense_medium_average = {}
# Simple dataFrame of medium and adsense revenue. Total, by channel, from the current
current_year = dataFrameSlice(adsense, {ym_key_pairs[11][1] : "origin"})
current_year = current_year.groupby('medium')['adsenserevenue'].sum()
current_year.sort_values(ascending=False, inplace=True, kind='quicksort', na_position='last')

# Creating a plot where the total adsense for the medium is divided by the number of sessions for session average.
# Plots average value of users based on current year, for the top five mediums.
for e in range(5):
    search_crit = current_year.index.values[e]
    medium_sum = adsense[adsense['medium'] == search_crit]['sessions'].sum()
    average_value = current_year[e] / medium_sum
    adsense_medium_average[search_crit] = average_value
makeBarPlot(sizeList, adsense_medium_average.values(), adsense_medium_average.keys(), "Average Cents by Channel", "Cents Per User", "US Cents")

#Creating a dictionary of average adsense revenue for country, from organic search.
country_adsense_value = {}
topPerformers = rankedDictionary(5, groupByDescending(adsense, ["country", "adsenserevenue"], 5)).keys() 
for performer in topPerformers:
    country_adsense_value[performer] = [] 
# Iterates through year-month combinations, finding average user value by country
for k, v in ym_key_pairs:
    for performer in topPerformers:
        #country_average = adsense[(adsense['country'] == performer) & (adsense['year'] == v) & (adsense['month'] == int(k))]['adsenserevenue'].sum() / adsense[(adsense['country'] == performer) & (adsense['year'] == v) & (adsense['month'] == int(k))]['sessions'].sum()
        country_average = dataFrameSlice(adsense, {v : 'origin', k : 'origin'}, {'country' : performer})['adsenserevenue'].sum() / dataFrameSlice(adsense, {v : 'origin', k : 'origin'}, {'country' : performer})['sessions'].sum()       
        temp = country_adsense_value[performer]
        temp.append(country_average)
        country_adsense_value[performer] = temp
        #print('\n' + country_adsense_value)
# Create a line plot for average "Organic Adsense Revenue by Country - Annual"        
makeLinePlot(sizeList, country_adsense_value, actual_months, "Organic Adsense Revenue by Country - Annual", 'Months', 'Average Adsense Earnings by Country')

# Sorted revenue dictionaries for all countries
#country_revenues = rankedDictionary(7, groupByDescending(organic, ["country", "adsenserevenue"], 7))
#country_sessions = rankedDictionary(len(set(organic['country'])), groupByDescending(organic, ["country", "sessions"], len(set(organic['country']))))
# Creates charts for the top five countries in each medium, filtered by 1000 sessions or more.

# Revenue by Medium
revenueByMedium(adsense, ym_key_pairs, "adsenserevenue")    

# Creating a plot of adsense revenue, by course, for the last year, for top 6 sources. 
current_year = dataFrameSlice(adsense, {ym_key_pairs[11][1] : "origin"})
source_sessions_dict = rankedDictionary(6, groupByDescending(current_year, ['source', 'adsenserevenue'], 6))
makeBarPlot(sizeList, source_sessions_dict.values(), source_sessions_dict.keys(), "Current Year Adsense by Source", "Sources", 'Total Adsense Last Year')    

# Slicing dataFrame and converting values to dictionary
data_currentMonth = adsense[(adsense['month'] == int(ym_key_pairs[11][0])) & (adsense['year'] == ym_key_pairs[11][1])]
data_currentMonth = dataFrameSlice(adsense, {ym_key_pairs[11][1] : 'origin', ym_key_pairs[11][0] : 'origin'})
source_sessions_dict = rankedDictionary(6, groupByDescending(data_currentMonth, ['source', 'adsenserevenue'], 6))
makeBarPlot(sizeList, source_sessions_dict.values(), source_sessions_dict.keys(), "Last Month", "Sources", 'Total Adsense Last Month')    

# Plotting the values of the top 6 sources
# Creating a slice of the dataFrame, grouped by sources, summed on revenues.
adsenseSources = adsense.groupby('source')['adsenserevenue'].sum()
adsenseSources.sort_values(ascending=False, inplace=True, kind='quicksort', na_position='last')

# Creating a plot_values dictionary and slicing on values in adsennseSources to return averages by source which can be forwarded to makeBarPlot. 
plot_values = {}
for e in range(8):
    source = adsenseSources.index.values[e]
    source_revenue = adsenseSources[e]
    # Creating a temporary dataframe, sessions, using the source, then summing on source to return the average.
    sessions = adsense.loc[adsense['source'] == source, 'sessions'].sum()
    actual_value = source_revenue / sessions
    plot_values[source] = actual_value
makeBarPlot(sizeList, plot_values.values(), plot_values.keys(), "Revenue Per Visitor", "Sources", "Revenues")