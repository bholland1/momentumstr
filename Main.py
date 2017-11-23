# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 18:05:34 2017

@author: brock
// --------------------------------------------------------------------
//
// Major Functions:	Main  
//
// --------------------------------------------------------------------
//
// Revision History :
// --------------------------------------------------------------------
//   Ver  :| Author            :| Mod. Date :| Changes Made:
//   V1.0 :| Brock             :| 03/25/2010:| Initial Revision

// --------------------------------------------------------------------
"""

from save_sp500_tickers import save_sp500_tickers
from get_data_from_yahoo import get_data_from_yahoo
from Ranker import ranker 

from Moving_average import Moving_average
from Moving_average import Index_moving_avr
from list_final import *




Trade = Index_moving_avr('^GSPC',200)
ticker_list = save_sp500_tickers()
#get_data_from_yahoo(ticker_list,200)
Rank_list = ranker(ticker_list)
List_Final = list_final(Rank_list,20,0.001,100000)