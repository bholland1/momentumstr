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


def allocation(ticker, ATR_period, risk_factor, funds_available):
    Addr = 'C:\\FinData\\S&P500\\TimeSeries'
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