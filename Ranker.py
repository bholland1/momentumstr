# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 17:40:23 2017

@author: brock
// --------------------------------------------------------------------
//
// Major Functions:	Ranker
//
// --------------------------------------------------------------------
//
// Revision History :
// --------------------------------------------------------------------
//   Ver  :| Author            :| Mod. Date :| Changes Made:
//   V1.0 :| Brock             :| 03/25/2010:| Initial Revision

// --------------------------------------------------------------------
"""
import csv 
import glob
import pandas as pd

from  momentum_ranking import momentum_ranking
from Moving_average import Moving_average


def ranker(tickers):
    list_c = []
    rank_list = []
    #need to change to local file directory
    file_dir = glob.glob('C:\\FinData\\S&P500\\TimeSeries\\*.csv')
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