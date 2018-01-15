# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 17:49:17 2017

@author: brock
// --------------------------------------------------------------------
//
// Major Functions:	Moving Average
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


def Moving_average(ticker,period):
    
    Moving_avr = ticker['CLOSE'].rolling(window=period).mean()
    if Moving_avr[-1] > ticker['CLOSE'][-1]:
        return False
    else:     
        return True
    
def Index_moving_avr(index,period,start,end):
    
    file_dir = 'C:\FinData\S&P500\\ConList\\'
    file_dir = file_dir + index + '.csv'
    Index = pd.read_csv(file_dir,index_col = 0)
    Index = Index[start:end]
    
    return Moving_average(Index,period)