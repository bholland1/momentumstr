# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 17:55:29 2017

@author: brock
// --------------------------------------------------------------------
//
// Major Functions:	Allocation 
//
// --------------------------------------------------------------------
//
// Revision History :
// --------------------------------------------------------------------
//   Ver  :| Author            :| Mod. Date :| Changes Made:
//   V1.0 :| Brock             :| 03/25/2010:| Initial Revision

// --------------------------------------------------------------------

"""
import pandas as pd
import csv


def allocation(ticker, ATR_period, risk_factor, funds_available,start,end):
    '''
    Generates an allocation for a given share, returning a single integer value
    e.g. 100 shares
    '''
    
    Addr = 'C:\\FinData\\S&P500\\TimeSeries1\\'
    Addr = Addr + ticker +'.csv'
    #print(ticker,start,end)
    ticker = pd.read_csv(Addr,index_col = 0)
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
    ticker = ticker[Sdate:Edate]         
    #Need dataset here
    ticker['ATR1'] = abs (ticker['HIGH'] - ticker['LOW'])  
    ticker['ATR2'] = abs (ticker['HIGH'] - ticker['CLOSE'].shift())
    ticker['ATR3'] = abs (ticker['LOW'] - ticker['CLOSE'].shift())
    ticker['TrueRange'] = ticker[['ATR1', 'ATR2', 'ATR3']].max(axis=1)    
    count = 0    
    TR_sum = 0   
    #print(ticker)
    while count < (len(ticker) - 1):
        TR_sum += ticker['TrueRange'][count]
        count += 1
    ticker['ATR'] = 0
    ticker['ATR'][0] = (1/len(ticker)) * TR_sum 
    count = 1
    while count < len(ticker['ATR']):
        ticker['ATR']= (ticker['ATR'].shift() * (len(ticker) -1) + ticker['TrueRange'])/(len(ticker))
        count +=1
    #print(ticker['ATR'])
    allocation = int((funds_available * risk_factor)/ticker['ATR'][-1])
    return (allocation)   