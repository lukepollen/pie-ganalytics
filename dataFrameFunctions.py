# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 15:15:56 2017

@author: dulce-senorita
"""

### Update dataFrameSlice to check if arguments supplied is greater than 2 for date/time and make a master frame if so.

from datetime import datetime
import os
from sqlalchemy import create_engine
import pandas as pd
from pandas.tseries.offsets import MonthEnd

def initializeDataFrame(tableType, startDate, columns):

    ### Targets the containing folder to build a reference to the correct database table, so a select * SQL query can be executed with the passed date up to today
    ### Example Use: data = initializeDataFrame("_source", "2016-01-01", "")
    absolute_path = os.getcwd()
    path_parts = absolute_path.split('\\')
    domain_name = path_parts[len(path_parts) - 1]
    domain_name = domain_name.partition(".")[0]
    # Final version of the table name, e.g. worldAnimalProtection_source
    table_name = domain_name + tableType    

    # Creating SQL command to retrieving data, based on range between string and today's date.
    today_date = datetime.today()
    today_date = today_date.strftime('%Y-%m-%d')
    query = "select * from " + table_name + " WHERE origin >= " + "'" + startDate + "'" + " AND origin < " + "'" + today_date + "'" + ';'
    engine = create_engine('postgresql://postgres:ve7arut5zaDr@localhost:5432/analytics')
    data = pd.read_sql_query(query, engine)
    data = data.drop_duplicates(subset=columns, keep='first', inplace=False)
    return data

def dateSliceGeneration():

    ### Generates a list of tuples which can be used to slice the DataFrames origin column.
    # go back in time twelve months periods (last day acceptable)
    now = datetime.now()
    end = now - MonthEnd()
    start = end - MonthEnd(11)
    dates = pd.date_range(start, end, freq='M')
    
    # Extract year and month from date range
    select_dict = {}
    
    for element in dates:
        element = pd.to_datetime(element)    
        year = element.year
        month = element.month
        select_dict[month] = year 
    
    # Creating a list of tuples with the month label and the year of the month.
    sorted_months = [k[0] for k in sorted(select_dict.items(), key=lambda kv: (kv[1], kv[0]))]
    originForm = {1 : "01", 2 : "02", 3 : "03", 4 : "04", 5 : "05", 6 : "06", 7 : "07", 8 : "08", 9 : "09", 10 : "10", 11 : "11", 12 : "12"}
    theMonths = []
    
    for element in sorted_months:
        theMonths.append(originForm[element])        
    
    sorted_years = [v[1] for v in sorted(select_dict.items(), key=lambda vk: (vk[1], vk[0]))]
    ym_key_pairs =  list(zip(theMonths, sorted_years))
    return ym_key_pairs
    
def monthRangeGeneration():

    months = {"01" : 'January', "02" : 'February', "03" : 'March', "04" : 'April', "05" : 'May', "06" : 'June', "07": 'July', "08" : 'August', "09" : 'September', "10" : 'October', "11" : 'November', "12" : 'December'}
    actual_months = []

    ym_key_pairs = dateSliceGeneration()
    for eachTuple in ym_key_pairs:
        actual_months.append(months.get(str(eachTuple[0])))
    return actual_months
    
def dataFrameSlice(dataFrame, sliceDict, *args):

    ### Slices dataFrame based on indices corresponding to the times in sliceDict, then on any column - rowvalue arguments in *args 
    ### Example Use: dataFrameSlice(data, {'2015' : 'origin', '05' : 'origin'})
    ### Example Use: dataFrameSlice(data, {'05' : 'origin'})
    indices = []
    if len(sliceDict.keys()) == 1:
        for key in sliceDict.keys():
            # Checks if value is for the month
            count = 0
            if len(str(key)) == 2:
                for element in dataFrame['origin']:
                    element = element.split("-")
                    if element[1] == str(key):
                        indices.append(dataFrame['id'].values[count])
                    count += 1
            # Proceeds if yearly value
            else:
                for element in dataFrame['origin']:
                    element = element.split("-")
                    if element[0] == str(key):
                        indices.append(dataFrame['id'].values[count])
                    count += 1
    # If two arguments are supplied, converts to list for indexing, then checks whether both element[0] and element[1] match.
    elif len(sliceDict.keys()) == 2:
        keyList = list(sliceDict.keys())
        # Position in dataframe's date column, origin
        count = 0
        for element in dataFrame['origin']:
            # Split the dates in the dataframe 'origin' column, so that they can be compared to the arguments supplied in the dictonary. 
            element = element.split("-")
            # If the distonary key values match with the year - month values, append the row to dataframe.            
            if str(element[0]) == str(keyList[0]) and str(element[1]) == str(keyList[1]): # Type conversion to string.
                # If there is a match, append the whole row to the dataframe
                #print("0 = 0 and 1 = 1")
                indices.append(dataFrame['id'].values[count])
            elif str(element[1]) == str(keyList[0]) and str(element[0]) == str(keyList[1]):
                #print("0 = 1 and 1 = 0")
                indices.append(dataFrame['id'].values[count])
            count += 1
    # Returns error message if more than one or two arguments are supplied.
    else:
        print("Please supply a month and a year argument only!")
        return
    # Slices dataFrame only if indices are not empty, otherwise would return empty dataFrame when date arguments are not provided
    if len(indices) > 0:
        dataFrame = dataFrame[dataFrame['id'].isin(indices)]
    # Returns an empty dataframe if indices are empty and arguments were supplied to sliceDict
    # Desired behaviour wherein no indices were found and time arguments were provided
    if len(indices) == 0 and len(sliceDict.keys()) > 0:
        dataFrame = dataFrame[dataFrame['id'].isin(indices)]
        return dataFrame
    if len(args) > 0:
        # Slicing the slice of time, based on any column - rowvalue values supplied to args
        ### Example Use: dataFrameTimeSlice(data, {'2015' : 'origin', '05' : 'origin'}, {"medium" : "referral", "socialnetwork" : "(notset)"})
        for e in args:
            for key in e.keys():
                dataFrame = dataFrame[dataFrame[key] == e[key]]
    return dataFrame                    
                        
def masterFrame(dataFrame, timeValues, *args):

    ### When a list of DataFrames are passed, the function performs a concatenation on the dataFrames
    ### Example Use: masterFrame(dataFrame, ym_key_pairs, {"medium" : "referral", "socialnetwork" : "(notset)"})

    # Creating a list of slices of the DataFrame for each year-month
    frameSlices = []
    for e in range(timeValues):
        theMonth = timeValues[e][0]
        theYear = timeValues[e][1]
        frameSlice = dataFrameSlice(dataFrame, {theMonth : "origin",  theYear: "origin"})
        frameSlices.append(frameSlice)
    
    # Reassigns dataFrame to the object resulting from concatenating only the values which matched the desired time range
    dataFrame = pd.concat(frameSlices)    
    # If a dictionary is supplied, call the dataFrame slice function with our dataFrame slice on time values and slice again on target columns matches rowvalues in the dictionary keys
    if len(args) > 0:
        for theDictionary in args:
            dataFrameSlice(dataFrame, {}, theDictionary)
    return dataFrame 
    
def groupByDescending(dataFrame, valueList, number):
    
    ### Groups the data by the criteria in the valueList, then returns then in descending order of the sum of the second valueList element
    ### Example Use: sourceSessions = groupByDescending(data, ['source', 'sessions'], number)
    rankedSummation = dataFrame.groupby(valueList[0])[valueList[1]].sum()
    rankedSummation.sort_values(ascending=False, inplace=True, kind='quicksort', na_position='last')
    rankedSummation = rankedSummation.head(n=number)
    return rankedSummation

def rankedDictionary(number, groupedDescending): # Need to add optional arguments to sort on values, rather than keys

    ### Returns a dictionary of the values returned by groupByDescending, with index labels as keys and label values as values.
    ### Example Use: rankedDictionary(6, sourceSessions)
    sortedDictionary = {}

    for element in range(number):
        sortedDictionary[groupedDescending.index.values[element]] = groupedDescending[element]

    #sortedDictionary = sorted(sortedDictionary, key=sortedDictionary.__getitem__, reverse=True)
    return sortedDictionary
   
    
    
                        

