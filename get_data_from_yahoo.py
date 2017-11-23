# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 17:34:03 2017

@author: brock
"""
import os
import csv 
from True_start_end_period import True_start_end_period

def get_data_from_yahoo(ticker_list,period):
    
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
   
    start, end = True_start_end_period(period)
       
    for ticker in ticker_list:
        
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = retry(web.DataReader)(ticker, "yahoo", start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker)) 
            
def retry(f, n_attempts=5):
    "Wrapper function to retry function calls in case of exceptions"
    def wrapper(*args, **kwargs):
        for i in range(n_attempts):
            try:
                return f(*args, **kwargs)
            except Exception:
                if i == n_attempts - 1:
                    raise
    return wrapper