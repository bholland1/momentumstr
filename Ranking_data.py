# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 09:03:47 2017

@author: brock
"""

#!/usr/bin/env python

import bs4 as bs
import pickle
import requests
import datetime
import os
import pandas as pd
import pandas_datareader.data as web
from pandas.tseries.offsets import BDay
import csv 
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
import statsmodels.api as sm
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style='ticks', context='talk')


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

def get_data_from_yahoo(reload_sp500=False):
    
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
        
    start = pd.datetime.today()- BDay(90)
    end = pd.datetime.today()
    
    for ticker in tickers:
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = retry(web.DataReader)(ticker, "yahoo", start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            #print('Already have {}'.format(ticker)) 
            b=1
            
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
            
def ranker(tickers):
    list_c = []
    rank_list = []
    #need to change to local file directory
    file_dir = glob.glob('C:\\Users\\brock\\Desktop\\Momentum\\stock_dfs\\*.csv')

    for file_name,j in zip(file_dir, tickers):
            ticker_data = pd.read_csv(file_name,index_col = 0)

            score = momentum_ranking(ticker_data)
            list_c.append(j) #need to retain name
            list_c.append(score)#retail score
            rank_list.append(list_c)
            list_c = []
            score = 0 
                
    rank_list = sorted(rank_list, key=lambda x: x[1], reverse = True)
    
    return rank_list

def momentum_ranking(ticker):      
    #print(ticker)
    ticker.head().round(2)
    ticker['Log'] =  np.log(ticker['Close'])
    ticker['Index'] = range(88)
    model = smf.ols(formula = "ticker['Log'] ~ ticker['Index']", data = ticker) 
    results = model.fit()
    R = results.rsquared
    slope = results.params[1]
    
    ann_slope = ((1 + slope)**252) - 1
    adj_slope = ann_slope * R
  #  print(R, ann_slope)
    return adj_slope



#quotes.append(retry(quotes_historical_google)(symbol, start_date, end_date))            
ticker_list = save_sp500_tickers()
get_data_from_yahoo()
Rank_list = ranker(ticker_list)

print(Rank_list)





