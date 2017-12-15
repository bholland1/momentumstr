# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 09:03:47 2017

@author: brock
"""

#!/usr/bin/env python

#import bs4 as bs
#import pickle
#import requests

import datetime
import os
import pandas as pd
import pandas_datareader.data as web
from pandas.tseries.offsets import BDay
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
import pandas_market_calendars as mcal

import csv 
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
import statsmodels.api as sm

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import glob
sns.set(style='ticks', context='talk')

##
def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    tickers[tickers.index('BRK.B')] = 'BRK-B'
    tickers[tickers.index('BF.B')] = 'BF-B'
    
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
    return tickers
##
def get_data_from_yahoo(ticker_list,period):
    
#    if reload_sp500:
#        tickers = save_sp500_tickers()
#    else:
#    with open("sp500tickers.pickle","rb") as f:
#        tickers_list = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
   
    start, end = True_start_end_period(period)
       
    for ticker in ticker_list:
        
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = retry(web.DataReader)(ticker, "yahoo", start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker)) 
 ##
def True_start_end_period(period, *start_date):
    ##In format --> start_data = 2017/10/30
    nyse = mcal.get_calendar('NYSE')
    period_init = period
    if not start_date:
        start = pd.datetime.today() - BDay(period_init)
        end = pd.datetime.today()
    else:
        start_date = start_date.split('/').split('-')
        start = pd.datetime(start_date[0],start_date[1],start_date[2]) - BDay(period_init)
        end = pd.datetime(start_date[0],start_date[1],start_date[2])
        
    dates = nyse.schedule(start_date=start, end_date=end)
    date_range = mcal.date_range(dates,frequency ='1D')
    ###   
    while(len(date_range) <= period_init):
        start = start - BDay(1)
        end = pd.datetime.today()
        dates = nyse.schedule(start_date=start, end_date=end)
        date_range = mcal.date_range(dates,frequency ='1D')
        
    return start, end
    
     ##      
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
 ##           
def ranker(tickers):
    list_c = []
    rank_list = []
    #need to change to local file directory
    file_dir = glob.glob('C:\\Users\\Brock\\Desktop\\momentum\\stock_dfs\\*.csv')
    tickers.sort()
    file_dir.sort()

    for file_name,j in zip(file_dir, tickers):
            ticker_data = pd.read_csv(file_name,index_col = 0)
            # test if ticker is trading below 100 day moving average
            moving_average = Moving_average(ticker_data,100)
            if not moving_average:
                pass
            else:
                score = momentum_ranking(ticker_data)
                list_c.append(j) #need to retain name
                list_c.append(score)#retail score
                list_c.append(ticker_data['Close'][-1])
                rank_list.append(list_c)
                list_c = []
            score = 0             
    rank_list = sorted(rank_list, key=lambda x: x[1], reverse = True)
    return rank_list
##
def momentum_ranking(ticker):      
    #print(ticker)
    ## Check for 15% price movement difference. 
    Change = ((ticker['Close'] - ticker['Open'].shift())/ticker['Close'])*100
    Price_diff = Change.loc[(Change >= 15)]
    if len(Price_diff) >= 1: 
        return -100  # or somthing equivalent to eliminate it from the list. 
    
    else:
        ticker.head().round(2)
        ticker['Log'] =  np.log(ticker['Close'])
        ticker['Index'] = range(len(ticker))
        model = smf.ols(formula = "ticker['Log'] ~ ticker['Index']", data = ticker) 
        results = model.fit()
        R = results.rsquared
        slope = results.params[1]
        ann_slope = ((1 + slope)**252) - 1
        adj_slope = ann_slope * R
        
        return (adj_slope)
    ##
def Moving_average(ticker,period):
    
    Moving_avr = ticker['Close'].rolling(window=period).mean()
    if Moving_avr[-1] > ticker['Close'][-1]:
        return False
    else:     
        return True
#########
def allocation(ticker, ATR_period, risk_factor, funds_available):
    Addr = 'C:\\Users\\Brock\\Documents\\momentumstr\\stock_dfs\\'
    Addr = Addr + ticker +'.csv'
    
    ticker = pd.read_csv(Addr,index_col = 0)
    #Need dataset here
    ticker['ATR1'] = abs (ticker['High'] - ticker['Low'])  
    ticker['ATR2'] = abs (ticker['High'] - ticker['Close'].shift())
    ticker['ATR3'] = abs (ticker['Low'] - ticker['Close'].shift())
    ticker['TrueRange'] = ticker[['ATR1', 'ATR2', 'ATR3']].max(axis=1)    
    count = 0    
    TR_sum = 0    
    
    while count < (ATR_period - 1):
        TR_sum += ticker['TrueRange'][count]
        count += 1
    
    ticker['ATR'] = 0
    ticker['ATR'][0] = (1/ATR_period) * TR_sum 
    count = 1
    while count < len(ticker['ATR']):
        ticker['ATR']= (ticker['ATR'].shift() * (ATR_period -1) + ticker['TrueRange'])/(ATR_period)
        count +=1

    allocation = int((funds_available * risk_factor)/ticker['ATR'][-1])
    return (allocation)   

###
def list_final(ticker, ATR_period, risk_factor, funds_available):
    '''
    Returns a final list with ticker, adj. slope and allocation of shares
    '''
    final_list = [] 
    funds_allocated = 0
    
    Rank_list = ranker(ticker_list)
     
    for i in Rank_list:
        funds_available = funds_available - funds_allocated
        funds_allocated = 0
        if funds_available <= 0:      
            return final_list
        else:
            shares = allocation(i[0], ATR_period, risk_factor, funds_available)
            funds_allocated = shares * i[2]
            Rank_list.append(shares)            
            Rank_list.append(funds_allocated)
            final_list.append(i)
    return final_list     

def Index_moving_avr(index,period):
    get_data_from_yahoo([index],period)
    
    file_dir = 'C:\\Users\\Brock\\Desktop\\momentum\\stock_dfs\\'
    file_dir = file_dir + index + '.csv'
    Index = pd.read_csv(file_dir,index_col = 0)
    return Moving_average(Index,period)
 


Trade = Index_moving_avr('^GSPC',200)
ticker_list = save_sp500_tickers()
get_data_from_yahoo(ticker_list,200)
Rank_list = ranker(ticker_list)