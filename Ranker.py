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


    ## Check for 15% price movement difference. 
    
    
    

def ranker(tickers,start, end):
    list_c = []
    rank_list = []
    #need to change to local file directory
    #file_dir = glob.glob('C:\\FinData\\S&P500\\TimeSeries\\*.csv')
    tickers.sort()
    
    for j in tickers:
            file_name = 'C:\\FinData\\S&P500\\TimeSeries1\\' + j + '.csv'
           #print(j)
            ticker_data = pd.read_csv(file_name,index_col = 0)
            # test if ticker is trading below 100 day moving average
            Sdate = start
            Sdate = Sdate.replace('/','-')
            if len(Sdate[:-8]) == 1:
                Sdate = Sdate[-4:] + '-' + Sdate[-7:-5] + '-'  + '0' + Sdate[:-8]
            else: 
                Sdate = Sdate[-4:] + '-' + Sdate[-7:-5] + '-' + Sdate[:-8]
            Edate = end
            Edate = Edate.replace('/','-')
            if len(Edate[:-8]) == 1:
                Edate = Edate[-4:] + '-' + Edate[-7:-5] + '-'  + '0' + Edate[:-8]
            else: 
                Edate = Edate[-4:] + '-' + Edate[-7:-5] + '-' + Edate[:-8]    
            ticker_data = ticker_data[Sdate:Edate]
            if len(ticker_data) < 20: 
                print('emergency')
                pass 
            elif len(ticker_data) < 100: #need to fix...  
                moving_average = Moving_average(ticker_data,len(ticker_data))
                ticker_data.reset_index()
                Change = abs(((ticker_data['OPEN'] - ticker_data['HIGH'].shift(1))/ticker_data['HIGH'].shift(1)))* 100
                #Change = abs(((ticker_data['CLOSE'] - ticker_data['OPEN'].shift())/ticker_data['CLOSE'])*100)
                Price_diff = Change.loc[(Change >= 15)]
                
                ticker_data.reset_index()
                k = 90 - len(ticker_data) 
                ticker_data = ticker_data[:k]
                
                score = momentum_ranking(ticker_data)
                list_c.append(j) #need to retain name
                list_c.append(score)#retail score
                list_c.append(ticker_data['CLOSE'][-1])# potential change to open 
                
                if len(Price_diff) >= 1: 
                    list_c.append('+/- 15 jump')
                elif(not moving_average): 
                    list_c.append('below 100 ma')          
                else: 
                    list_c.append('fine')
                rank_list.append(list_c)  
            else:      
                moving_average = Moving_average(ticker_data,100)
                Change = abs(((ticker_data['OPEN'] - ticker_data['HIGH'].shift(1))/ticker_data['HIGH'].shift(1)))* 100
                #Change = abs(((ticker_data['CLOSE'] - ticker_data['OPEN'].shift())/ticker_data['CLOSE'])*100)
                Price_diff = Change.loc[(Change >= 15)]
                
                ticker_data.reset_index()
                ticker_data = ticker_data[:-10]
                score = momentum_ranking(ticker_data)
                list_c.append(j) #need to retain name
                list_c.append(score)#retail score
                list_c.append(ticker_data['CLOSE'][-1])# potential change to open 
                
                if len(Price_diff) >= 1: 
                    list_c.append('+/- 15 jump')
                elif(not moving_average): 
                    list_c.append('below 100 ma')          
                else: 
                    list_c.append('fine')
                    
                rank_list.append(list_c)   
            list_c = []
            score = 0   
    #print(rank_list)
    rank_list = sorted(rank_list, key=lambda x: x[1], reverse = True)
    return rank_list




