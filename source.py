# -*- coding: utf-8 -*-
"""
Created on Mon Jan 04 13:50:05 2016

@author: Anima
"""

# Update period comparison to state time comparison
from displayfunctions import month_compare, period_compare
from plotfunctions import makeBarPlot, makeLinePlot, dataFrameXTicks
from dataFrameFunctions import groupByDescending, dataFrameSlice, dateSliceGeneration, initializeDataFrame, monthRangeGeneration

### Default Variables
sizeList = [12, 6]    
    
### Data Load
data = initializeDataFrame("_keywords", "2017-09-01", ['medium', 'source', 'socialnetwork', 'sessions', 'avgsessionduration', 'pageviews', 'bouncerate', 'pageviewspersession', 'origin'])
        
ym_key_pairs = dateSliceGeneration()
actual_months = monthRangeGeneration()

### Charting Data
total_list = []
organic_list = dataFrameXTicks(data, ym_key_pairs, ['medium', 'organic'], 8)
# The positive argument means only dataframes whose socialnetwork column with value equal to "(not set)" is included.
referral_list = dataFrameXTicks(data, ym_key_pairs, ['medium', 'referral'], 8, "socialnetwork", "(not set)", "positive")
# Targeting the social networks.
social_list = dataFrameXTicks(data, ym_key_pairs, ['medium', 'referral'], 8, "socialnetwork", "(not set)", "negative")
direct_list = dataFrameXTicks(data, ym_key_pairs, ['medium', '(none)'], 8) 
cpc_list = dataFrameXTicks(data, ym_key_pairs, ['medium', 'cpc'], 8)

# Creating sum of the elements at each nth location in the respect list.
for i in range(len(organic_list)):
    fig = organic_list[i] + referral_list[i] + social_list[i] + direct_list[i] + cpc_list[i]
    total_list.append(fig)

# Dictionary container
channelValues = {
'Total' : total_list, 
'Search Engine' : organic_list,
'Referral' : referral_list,
'Social' : social_list,
'Direct' : direct_list,
'PPC' : cpc_list                 
}

# Plotting all lists.
makeLinePlot(sizeList, channelValues, actual_months, "Website Traffic - By Channel", "Months", "Sessions")
period_compare(total_list)
month_compare(total_list)

# Plotting the Organic data for the last year and printing comparison for the last year and the last month versus previous.    
makeBarPlot(sizeList, organic_list, actual_months, "Organic", "Months", "Sessions")
period_compare(organic_list)
month_compare(organic_list)

# Referral plot for last year
makeBarPlot(sizeList, referral_list, actual_months, "Referral", "Months", "Sessions")
period_compare(referral_list)
month_compare(referral_list)

# Social media plot for last year
makeBarPlot(sizeList, social_list, actual_months, "Social Media", "Months", "Sessions")
period_compare(social_list)
month_compare(social_list)

# Direct plot for last year
makeBarPlot(sizeList, direct_list, actual_months, "Direct", "Months", "Sessions")
period_compare(direct_list)
month_compare(direct_list)

# PPC plot for last year
makeBarPlot(sizeList, cpc_list, actual_months, "Pay Per Click", "Months", "Sessions")
period_compare(cpc_list)
month_compare(cpc_list)

### Needs to be expanded to go back last twelve months. Currently only uses data points that exist in current year.
# Four the last year, select the last six sessions by sum of sources and return in descending order.
data_year = dataFrameSlice(data, {ym_key_pairs[11][1] : 'origin'})
top_source_sessions = groupByDescending(data_year, ['source', 'sessions'], 8)

# Creating a dictionary of source : sourceSessions to plot from.
source_sessions_dict = {}
for e in range(6):
    source_sessions_dict[top_source_sessions.index.values[e]] = top_source_sessions[e]
    
# Plotting the top sources
makeBarPlot(sizeList, source_sessions_dict.values(), list(source_sessions_dict.keys()), "Top Sources Last Year", "Sessions", "Sources This Year")

# Selecting based on the last year AND the last month
data_month = dataFrameSlice(data, {ym_key_pairs[11][1] : 'origin', ym_key_pairs[11][0] : 'origin'})
top_source_sessions = groupByDescending(data_month, ['source', 'sessions'], 8)
source_sessions_dict = {}

# Reapeating plot of source : sourceSessions, but for the last month as opposed to last year.
for e in range(6):
    source_sessions_dict[top_source_sessions.index.values[e]] = top_source_sessions[e]

# Plotting top sources for last month.    
makeBarPlot(sizeList, source_sessions_dict.values(), list(source_sessions_dict.keys()), "Top Sources Last Month", "Sessions", "Sources This Month")