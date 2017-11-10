# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 08:52:10 2017

@author: Brock

Backtesting Funct. 
"""
import datetime
import pandas as pd
import pandas_datareader.data as web
from pandas.tseries.offsets import BDay





def back_test(Inital_Capital,start,end,transaction_cost,slippage_factor):
"""
This function peforms the nesicarry back testing needed for robust testing of 
the stratergy. 
Proceduraly, it works as follows: 
    Gathers 90 day price data from all S&P500 (or other companies):
    Performs ranking calculations.
    Complies a list of allocations.
    Executes a trade on these allocations.
    Populates a PDF of a summary of positions, trades, money and portfolio.
    movement/value against the index. 
    
    Performs execution again and repeats over the duraction of the start-end 
    dates.
"""
    final = end
    90_day_start = start
    90_day_end = 90_day_start + Bday(90)

    while(90_day_end < final):
        data = get_data(index,90_day_start,90_day_end)
        Rank_list = ranker(data)
        Allocation_list = Allocation(Rank_list)
        PDF_Summary()
        
        90_day_start = 90_day_start + BDay(90)       
        90_dat_end = 90_day_start + BDay(90)
        
    
    return 





def get_data(index):
"""
This function returns the data from a specified duration of all price data for
all companies traded on an index. 
"""
    return 