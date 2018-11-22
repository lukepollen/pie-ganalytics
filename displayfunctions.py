# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 16:04:40 2017

@author: Cortica
"""

import pandas as pd

### Global Values

colorred = "\033[01;31m{0}\033[00m"
colorgrn = "\033[1;36m{0}\033[00m"

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')
    
def month_compare(the_list):
    total = sum(the_list)
    if total == 0:
        return None
    else:
        first = the_list[len(the_list)-1]
        first_as_float = float(first)    
        second = the_list[len(the_list)-2]
        second_as_float = float(second)
        pct_change = round((100 / second_as_float) * first_as_float, 2) - 100
        if pct_change >= 0:
            print(colorgrn.format(str(pct_change) + '% Monthly Increase!'))
        else:
            print(colorred.format(str(pct_change) + "% Monthly Decrease!"))
        
def period_compare(the_list):
    total = sum(the_list)    
    if total == 0:
        return None        
    else:
        first_sum = sum(the_list[int(len(the_list) / 2):])    
        first_list = float(first_sum)
        second_sum = sum(the_list[:int(len(the_list) / 2)])
        second_list = float(second_sum)
        pct_change = round((100 / float(second_list)) * first_list, 2) - 100
        if pct_change >= 0: 
            print(colorgrn.format(str(pct_change) + '% Period Increase!'))
        else:
            print(colorred.format(str(pct_change) + '% Period Decrease!'))