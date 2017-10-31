# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 19:22:18 2017

@author: Aaron
"""
import csv 
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
import statsmodels.api as sm
import os
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style='ticks', context='talk')


if int(os.environ.get("MODERN_PANDAS_EPUB", 0)):
    import prep # noqa




file = open('constituents.csv')
reader = csv.reader(file)
SP500 = list(reader)
SP500.remove(SP500[0]) 


def ranker():
    list_c = []
    rank_list = []
    count = 0
    while count < 5:
            print(SP500[count][0])
            score = momentum_ranking(SP500[count][0])
            list_c.append(SP500[count][0])
            list_c.append(score)
            rank_list.append(list_c)
            list_c = []
            score = 0
            count += 1
            
    rank_list = sorted(rank_list, key=lambda x: x[1], reverse = True)
    return rank_list





def momentum_ranking(ticker):
    ticker = web.DataReader(ticker, data_source='yahoo', start='2017-06-23',
                        end='2017-10-29')
    ticker.head().round(2)
    ticker['Log'] =  np.log(ticker['Close'])
    ticker['Index'] = range(90)
    
    model = smf.ols(formula = "ticker['Log'] ~ ticker['Index']", data = ticker) 
    results = model.fit()
    R = results.rsquared
    slope = results.params[1]
    
    ann_slope = ((1 + slope)**252) - 1
    adj_slope = ann_slope * R
    print(R, ann_slope)
    return adj_slope

    
    
        
    
