# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 08:52:10 2017

@author: Brock

Backtesting Funct. 
"""
import datetime
import pandas as pd
from pydatastream import Datastream
from pandas.tseries.offsets import BDay


from save_sp500_tickers import save_sp500_tickers
from get_data_from_yahoo import get_data_from_yahoo
from Ranker import ranker 
from list_final import *

from Moving_average import Moving_average
from Moving_average import Index_moving_avr



def back_test(Inital_Capital, start, end, transaction_cost, slippage_factor, trade_interval):
    """
This function peforms the necessary back testing needed for robust testing of 
the strategy. 
Proceduraly, it works as follows:
    If the Index is below its 200 day MA, do nothing, else

    Initially, it ranks all members of the index based on the ranking parameters (adj. slope or others)
    If the stock is trading below its 100 day MA or had a gap in excess of 15%, it cant be bought
    Will then generate a portfolio using the allocation function, and buy at next days open
    
    At next interval date, will rebalance/buy/sell where needed:
        First, we check for selling: --> DONE
            If any holding has dropped out of the top 20% of ranked stocks,
            is trading below its 100 day MA, has had a gap of 15% or more, or
            dropped out of the index, then we liquidate the position.
            
        Next we check for rebalancing (only every second week): 
            We check for each holding whether our current position size matches our
            target position size. If it is close enough (what does that mean?),
            dont rebalance, if it is far away, rebalance to target weight
            (either add to or reduce position).
            
        Lastly, we check for buying:        
            If we have liquidity from selling holdings, we buy (provided we are allowed).
            We go down the current ranking list and allocate funds based on target weightings.
            If we already hold a position in that stock, we move on.
            Keep buying until no funds left
            
        Performance tracking:
            A few ways:
                (Every day? Week?)
                - Could just have a simple tracker which stores the total 
                portfolio value over time
                - Cumulative returns
                - Need a record of every trade made, when position entered and exited
    
    """
# For csv file, there is a row entry for each day, and column entries of each ticker
# in the index that day.
# We iterate through this file.
# For each specified interval, we make a ranking for the members in the index that day
# Form portfolio based off of this ranking list.
# Price data for each member over the entire period is stored in a seperate location to be accessed anytime.
    return 

# open constituents list 
'''------------------BACK TESTING PARAMETERS------------------------------- '''
rebalance_period = 10 #BUISNESS DAYS 
StartingLiquidity = 100000 #US Dollars 
RiskFactor = 0.001
AverageTrueRangePeriod = 20 
UpdateThresh = 0.1
'''----------------------FILE NAMES---------------------------------------- '''
CONSLIST = 'C:\\FinData\\S&P500\\ConList\\Final.csv'
INDEX = 'C:\FinData\S&P500\\SP500.csv'

'''----------------------INITAL VARIABLES---------------------------------- '''
Holdings = []
Liquidity = StartingLiquidity

cons = pd.read_csv(CONSLIST)
SP500 = pd.read_csv(INDEX)

for index, row in cons.iterrows():
    #execute algo every 10 buisness days 
    if( (index % rebalance_period) == 0 and index != 0 ): 
        ticker_list = []
        for j in row[2:]: # gets rid of @: from ticker list
            A = j
            if(type(A) == str): 
                ticker_list.append(A.replace('@:',''))
            else:
                pass
        #Trade = Index_moving_avr('^GSPC',200)    
        Rank_list = ranker(ticker_list)
        SuggestedPos = list_final(Rank_list,AverageTrueRangePeriod,RiskFactor,StartingLiquidity)
        '''----------------SELLING -----------------------------------------'''
        # check if any current holdings are below the top 20%, then sell positions 
        #is trading below its 100 day MA, has had a gap of 15% or more, or
        # dropped out of the index, then we liquidate the position.
        ### INSERT CODE HERE ###
        rank_length = len(Rank_list) 
        len_quintle = rank_length/5 
        top_quintile = Rank_list[0:len_quintle]
        
        for i in range(0,len(Holdings)): 
            for j in range(0, len_quintle):
                if(Holdings[i][0] not in top_quintile[j][0]): 
                    Liquidity += Holdings[3] # ADD SAID POSITION TO CAPITAL 
                    Holdings.remove(Holdings[i]) 
                    # record...
                else: 
                    pass
        for i in Rank_list: 
            for j,index in zip (Holdings, range(0,len(Holdings))): 
                if(i[0] == j[0]):
                    if(i[-1] == 'fine'):
                        pass
                    else: 
                        Liquidity += Holdings[3] # ADD SAID POSITION TO CAPITAL
                        Holdings.remove(Holdings[index])
                        #record... 
        '''----------------UPDATE HOLDINGS----------------------------------'''       
        # UPDATE POSITIONS: COMPARE THE HOLDINGS AND SIZE OF EACH TICKER AND RE
        # NEGATICE REBALLANCING:lIQUIDATE IF POSITION IS OUTSIDE A CERTAIN PERCENT RANGE. 
        #

        ### INSERT CODE HERE ###
        for i in SuggestedPos: 
            for j in range(0,len(Holdings)):
                if (i[0] == Holdings[j][0]): 
                    if(((i[2] - Holdings[j][2])/i[2]) <= -UpdateThresh):# below current position
                        SharesToBeSold = Holdings[j][2] - i[2]
                        Liquidity += SharesToBeSold*Holdings[j][3] # times by open price
                        Holdings[j][2] = i[2]
                        Holdings[j][4] = Holdings[j][2]*Holdings[j][3]
                        
        # POSITIVE REBALANCING: WITH NEWLY AQUIRED FUNDS, START REBALANCING FROM 
        # BASED ON CURRENT POSITIONS  
        for i in SuggestedPos: 
            for j in range(0,len(Holdings)):
                if (i[0] == Holdings[j][0]): 
                    if(((i[2] - Holdings[j][2])/i[2]) <= UpdateThresh):# below current position
                        SharesToBePurchased = i[2] - Holdings[j][2]  
                        Liquidity -= SharesToBePurchased*Holdings[j][3] # times by open price
                        Holdings[j][2] = i[2]
                        Holdings[j][4] = Holdings[j][2]*Holdings[j][3]                     
        
        # ENTERING NEW POSITIONS: IF THERE ARE ANY FUNDS STILL AVALIABLE, BUY 
        # NEW POSITIONS FROM TOP OF LIST. 
        newPose = True 
        if(Liquidity > 0): 
            for i in SuggestedPos: 
                for j in Holdings: 
                    if(i[0] not in j): 
                        newPos = False
                    else: 
                        newPos = True
                if(newPos): 
                    list_new = [i] 
                    Holdings.append(list_new)
        else: 
            pass 
            
        '''----------------PERFORMANCE MEASURING----------------------------''' 
        # INVEST A DOLLAR IN INDEX AND DOLLAR IN STRATERGY THEN PLOT RETURNS. 
        
        
    else: 
        pass 
    
    '''----------------PERFORMANCE MEASURING----------------------------''' 
    # INVEST A DOLLAR IN INDEX AND DOLLAR IN STRATERGY THEN PLOT RETURNS. 