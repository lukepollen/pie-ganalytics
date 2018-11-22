# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 14:48:49 2017

@author: Cortica
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

### Plotting Functions 
def makeBarPlot(sizeList, barList, xTickLabelsList, title, xLabel, yLabel):
   
    ### Makes a matplotlib bar plot
    ### Example Use: makeBarPlot(sizeList, sums, actual_months, "Organic", "Months", "Sessions")
    plt.figure(figsize=(sizeList[0], sizeList[1]))
    plt.bar(range(len(barList)), barList, align='center')
    plt.xticks(range(len(barList)), xTickLabelsList, size='small')
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.tight_layout()
    plt.show()    
    
def makeLinePlot(sizeList, valueDictionary, xTickLabelsList, title, xLabel, yLabel):
    
    ### Makes a matplotlib line plot
    ### Example Use: makeLinePlot(sizeList, channelValues, actual_months, "Website Traffic - By Channel", "Months", "Sessions")
    plt.figure(figsize=(sizeList[0], sizeList[1]))
    plt.xticks(range(len(xTickLabelsList)), xTickLabelsList, size='small')
    for eachList in valueDictionary.values():
        plt.plot(eachList)
    plt.title(title)
    plt.ylabel(yLabel)
    plt.xlabel(xLabel)
    plt.legend(valueDictionary.keys(), loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True)    
    plt.tight_layout()
    plt.show()
    
def dataFrameXTicks(dataFrame, tupleList, interestColumnList, sumColumn, *args):

    ### Slices a pandas dataFrame according to the passed arguments. Returns a list for matplotlib plotting.
    ### Example Use: dataFrameXTicks(data, ym_key_pairs, ['medium', 'organic'], 8, "socialnetwork", "(not set)", "negative")
    
    # Fragmenting dataFrame based on the column of interest:
    dataFrame = dataFrame[dataFrame[interestColumnList[0]] == interestColumnList[1]]
    if len(args) > 0:
        # If the third conditional argument is "negative", slice the dataframe by first conditional argument
        if args[2] == "negative":
            # Only return where, for example, "socialnetwork" != "(not set)". Dataframe shrunk to social networks only.
            dataFrame = dataFrame[dataFrame[args[0]] != args[1]]
            #print(dataFrame)
        else:    
            dataFrame = dataFrame[dataFrame[args[0]] == args[1]]    
    # list of values to return for plotting
    sums = []
    # Iterating through the year-month values
    for k, v in tupleList: 
        # Empty list of individual sessions which will be populated by row values which match the k, v year-month criteria
        sessionSum = []
        count = 0
        # Begin splitting date strings:        
        for element in dataFrame['origin']:
            element = element.split("-")
            # If the split element list matches both the year and month criteria, add the count to the temporary list to sum. 
            if str(element[1]) == str(k):
                if str(element[0]) == str(v):                    
                    # Adding each session to the summation list.
                    sessionSum.append(dataFrame.iloc[count][sumColumn])
            count += 1
        # Summing the summation list for a final figure, which can be used in our final plot.         
        sums.append(sum(sessionSum))
        print(sum(sessionSum))
    return sums
    
def revenueByMedium(dataFrame, yearMonthTuples, revenue):

    ### Prints revenue by medium for a dataframe with a revenue, session and medium column
    ### Example use: RevenueByMedium(adsense, ym_key_pairs, "adsenserevenue")
    country_medium_values = {}
    
    last_year = dataFrame[dataFrame['year'] == yearMonthTuples[11][1]]
    last_year = last_year.groupby('medium')[revenue].sum()
    last_year.sort_values(ascending=False, inplace=True, kind='quicksort', na_position='last')
    
    for medium in last_year.index.values:
        med = dataFrame[dataFrame['medium'] == medium]
        country_revenues = med.groupby('country')[revenue].sum()
        country_sessions = med.groupby('country')['sessions'].sum()
        countries = []
        country_adsense_value = {}
        count = -1
        for e in country_sessions:
            count += 1
            if e >= 100:
                countries.append(country_sessions.index.values[count])
            else:
                continue
        for e in countries:
            try:
                country_average = country_revenues[e] / country_sessions[e]
                country_total = round(country_average * 1000, 2)
            except KeyError:
                continue
            country_adsense_value[e] = country_total
        country_medium_values[medium] = country_adsense_value 

    print('\n' + 'Revenues Per Thousand by Medium') 
        
    for medium in country_medium_values.keys():
        top_country_mediums = sorted(country_medium_values[medium].items(), key=lambda x:-x[1])[:5]
    
        print('\n' + medium + ':')
        for x in top_country_mediums:
            print("{0}: {1}".format(*x))
            
    count = -1
    selector = list(country_medium_values.keys())
    
    for medium in country_medium_values.keys():
        try:
            top_country_mediums = sorted(country_medium_values[medium].items(), key=lambda x:-x[1])[:5]
            countries = []
            dollars = []
            for e in top_country_mediums:
                countries.append(e[0])
                dollars.append(e[1])
            count += 1
            df = pd.DataFrame(dict(graph=countries, m=dollars))
            ind = np.arange(len(df))
            width = 0.4

            fig, ax = plt.subplots()
            ax.barh(ind + width, df.m, width, color='red', label=selector[count])

            ax.set(yticks=ind + width, yticklabels=df.graph, ylim=[2*width - 1, len(df)])
            ax.legend()

            plt.title('Dollars Per Thousand Sessions')
            plt.show()
        except:
            pass
    