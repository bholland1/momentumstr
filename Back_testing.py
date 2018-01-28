# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 08:52:10 2017

@author: Brock

Backtesting Funct. 
"""
import csv
import datetime
import pandas as pd
from pydatastream import Datastream


from Ranker import ranker 
from list_final import *

from Moving_average import Moving_average
from Moving_average import Index_moving_avr

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

# open constituents list---> '1991-01-22'<---
'''----------------------FILE NAMES---------------------------------------- '''
CONSLIST = 'C:\\FinData\\S&P500\\ConList\\Final_DoW3.csv'
INDEX = 'C:\FinData\S&P500\\ConList\\SP500_1.csv'
TICKERNAMES = 'C:\\FinData\\S&P500\\all.csv'
'''------------------BACK TESTING PARAMETERS------------------------------- '''
Start_date =  '5/01/1998'#'1999-01-02'#pd.to_datetime('1999-01-02')#datetime.date(1999, 01, 02) #
End_date =  '30/12/2016' #'2014-12-31' #pd.to_datetime('2014-12-31')# datetime.date(2014, 12, 31) #
rebalance_period = 10 #BUISNESS DAYS 
StartingLiquidity = 100000 #US Dollars 
PortfolioValue = StartingLiquidity
Liquidity = StartingLiquidity
PrevLiquidity = 0 
RiskFactor = 0.001
AverageTrueRangePeriod = 20 
UpdateThresh = 0.2
momentumPeriod = 100 
Trade = True
'''TRADING RECORDERS ''' 
POSENTERED = 0 
POSENTEREDVAL = 0
NEGREBAL = 0
NEGREBALVAL = 0
POSREBAL = 0
POSREBALVAL = 0
SELLQUINT = 0
SELLQUINTVAL = 0
SELLMA = 0 
SELLBEL100MA = 0
secondWeek = 0
'''----------------------INITAL VARIABLES---------------------------------- '''
'''HOLDINGS''' 
Holdings = [] # Portfolio Holdings
HoldingsRecord = open("HoldingsRecord.csv",'w')
wr = csv.writer(HoldingsRecord, dialect = 'excel')
'''PORTFOLIO AND SP500 VALUE TRACKERS ''' 
SP500Value = 0 
SPportfolioVal = StartingLiquidity
SP500ValList = [StartingLiquidity] # Array of portfolio Value over time
PortfolioValList = [StartingLiquidity] # Array of SP500 value over time 
'''CONSTITUENT LIST OF SP500 AND SP500 DATA FRAMES'''
cons = pd.read_csv(CONSLIST,index_col = 0)
cons = cons[Start_date:End_date]
cons = cons.reset_index()
cons.rename(columns={'Unnamed: 1': 'Date', 'Unnamed: 2': 'Day'}, inplace=True)
SP500 = pd.read_csv(INDEX, index_col = 0)
SP500 = SP500[Start_date:End_date]
SP500 = SP500.reset_index()
SP500.rename(columns = {'index': 'date'}, inplace = True)
ticnam = pd.read_csv(TICKERNAMES)
SP500ValList.append(Liquidity)
PortfolioValList.append(Liquidity)
'''SETTING UP THE MONTHLY RETURNS DATA FRAME''' 
PortfolioValSeries = pd.DataFrame(SP500['date'])
PortfolioValSeries['value'] = 'nan'



columns = ['year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Anual']
df = pd.DataFrame({'year': [1999,2000,2001,2002,2003,2004,
    2005,2006,2007,2008,2009,2010,2011,2012, 2014, 2013, 2014,2015,2016,2017]},columns=columns)
df = df.set_index('year')
Year = int(Start_date[-4:]) + 1 #YEAR THAT MONTHLY RETURNS ARE STARTING TO BE RECORDED
Month = '01' #TYPICALLY START THE RETURN RECORDING AT THE START OF THE YEAR
M = 'Jan'
StartMonth = Liquidity
StartYear = Liquidity
StartVal = Liquidity # USED TO CALUCALATE VALUE AT THE START AND END OF MONTHS
EndVal  = 0
B = False

'''!!!!SIMULATION STARTS!!!!'''
for index, row in cons.iterrows():
    if row[0] == '4/01/1999': # make this the first day you want to establish a  portfolio.
        B = True              # NOTE THAT THIS MUST BE 200 DAYS AHEAD OF THE START_DATE
    if B:  
        '''------- UPDATE PORTFOLIO VALUE---------------------------------- ''' 
        if len(Holdings) > 0:
            Holdings_copy = Holdings[:]
            for i, Index in zip(Holdings_copy, range(len(Holdings))): 
                addr = 'C:\FinData\S&P500\\TimeSeries1\\' + i[0] + '.csv'
                ticker = pd.read_csv(addr)
                date = row[0][:]
                date = date.replace('/','-')
                if len(date[:-8]) == 1:
                    date = date[-4:] + '-' + date[-7:-5] + '-'  + '0' + date[:-8]
                else: 
                    date = date[-4:] + '-' + date[-7:-5] + '-' + date[:-8]
                A = len(ticker.loc[ticker['Unnamed: 0'] == date])
                if A == 0:
                    pass
                else:
                    ticker = pd.read_csv(addr, index_col = 0)
                    price = ticker['CLOSE'][date]
                    Holdings[Index][2] = price
                    Holdings[Index][5] = Holdings[Index][2]*Holdings[Index][4]
            Holdings_copy = []        
            PortfolioValue = 0
            for i in Holdings:
                PortfolioValue += i[5]
            PortfolioValue += Liquidity
        '''---------------STRATERGY EXECUTION-------------------- '''        
    #execute algo every second wedensday 
    if row[1] == 4:
        secondWeek += 1
        if secondWeek == 2 and not B :
            secondWeek = 0   
    '''BUY AND SELL EVERY WEDNESDAY'''         
    if(row[1] == 4 and B):   
        PrevLiquidity = Liquidity
        ticker_list = []
        for j in row[2:]: # gets rid of @: from ticker list
            A = j
            if(type(A) == str): 
                ticker_list.append(A.replace('@:',''))
            else:
                pass
        ticker_list = [i for i in ticker_list if i not in #quick fix need to fix on data end
        ('0','AHM','CTCO','GEB','GNN','HBJ','HIA','MCA','ML','NRT','GW','PHL','PCSW','XP','SQD','WETT','CSGA','STJM','PN')] 
        end_r = SP500['date'][index]
        start_r = SP500['date'][(index - (momentumPeriod-1))]
        end_f = SP500['date'][index]
        start_f = SP500['date'][(index - (AverageTrueRangePeriod-1))]
        
        Trade = Index_moving_avr('SP500_1',200, SP500['date'][index - 199], SP500['date'][index])    
        Rank_list = ranker(ticker_list,start_r,end_r)
        Rank_list2 = Rank_list[:]
        A = []
        for i in range(len(Rank_list)):
            if Rank_list[i][3] == 'below 100 ma' or Rank_list[i][3] == '+/- 15 jump' or Rank_list[i][3] == 'Not enough data': 
                A.append(i)
            else:
                pass
        for j in A[::-1]:
            del Rank_list2[j]
        SuggestedPos = list_final(Rank_list2,AverageTrueRangePeriod,RiskFactor,PortfolioValue,start_f,end_f)
        '''----------------SELLING ----------------------------------------------------
        -------------------------------------------------------------------------------
        ----------------------------------------------------------------------------'''   
        # check if any current holdings are below the top 20%, then sell positions 
        #is trading below its 100 day MA, has had a gap of 15% or more, or
        # dropped out of the index, then we liquidate the position.
        ### INSERT CODE HERE ###
        QuintTickList = []
        rank_length = len(Rank_list)
        len_quintle = rank_length//5
        top_quintile = Rank_list[0:len_quintle]
        for i in top_quintile:
            QuintTickList.append(i[0])
        quintile_tickers = []
        if(len(Holdings) == 0):
            pass 
        else: 
            for j in range(len_quintle):
                quintile_tickers.append(top_quintile[j][0])
            for i in range(len(Holdings)):   
                if(Holdings[i][0] not in quintile_tickers): 
                    Liquidity += Holdings[i][5] # ADD SAID POSITION TO CAPITAL 
                    SELLQUINTVAL += Holdings[i][5]
                    Holdings[i][5] = 0
                    # record...
                    SELLQUINT += 1
                else: 
                    pass
            A = []
            for i in range(len(Holdings)):
                if Holdings[i][5] == 0:
                    A.append(i)
                else:
                    pass
            for j in A[::-1]:
                del Holdings[j]
                
            if(len(Holdings) > 0):    
                for i in Rank_list: 
                    for j,a in zip (Holdings, range(len(Holdings))): 
                        if(i[0] == j[0]):
                            if(i[3] == 'fine'):
                                pass
                            else: 
                                Liquidity += Holdings[a][5] # ADD SAID POSITION TO CAPITAL
                                SELLBEL100MA += Holdings[a][5]
                                Holdings[a][5] = 0
                                SELLMA += 1

                    A = []
                    for i in range(len(Holdings)):
                        if Holdings[i][5] == 0: 
                            A.append(i)
                        else:
                            pass
                    for j in A[::-1]:
                        del Holdings[j]            
                            #record... 
        '''---------------------------UPDATE HOLDINGS----------------------------------
        -------------------------------------------------------------------------------
        -------------------------------------------------------------------------------
        ----------------------------------------------------------------------------''' 
        '''UPDDATE POSITION EVERY SECOND WEDENSDAY'''     
# UPDATE POSITIONS: COMPARE THE HOLDINGS AND SIZE OF EACH TICKER AND RE
        if secondWeek == 2: 
            secondWeek = 0
            '''----------------------------Negative Rebalance----------------------------'''
# NEGATICE REBALLANCING:lIQUIDATE IF POSITION IS OUTSIDE A CERTAIN PERCENT RANGE.
            if len(Holdings) > 0: 
                for i in SuggestedPos: 
                    for j in range(0,len(Holdings)):
                        if (i[0] == Holdings[j][0]): 
                            if(((i[4] - Holdings[j][4])/i[4]) <= -UpdateThresh):# below current position
                                SharesToBeSold = Holdings[j][4] - i[4]
                                Liquidity += SharesToBeSold*i[2] # times by open price
                                Holdings[j][2] = i[2]
                                Holdings[j][4] -= SharesToBeSold
                                Holdings[j][5] = Holdings[j][2]*Holdings[j][4]
                                NEGREBAL += 1
                                NEGREBALVAL += SharesToBeSold*Holdings[j][2]
            '''----------------------------Positive Rebalance----------------------------'''                                
# POSITIVE REBALANCING: WITH NEWLY AQUIRED FUNDS, START REBALANCING FROM 
# BASED ON CURRENT POSITIONS  
            if Trade and len(Holdings) > 0:
                for i in SuggestedPos: 
                    for j in range(len(Holdings)):
                        if (i[0] == Holdings[j][0]): 
                            if(((i[4] - Holdings[j][4])/i[4]) >= UpdateThresh):# below current position
                                SharesToBePurchased = i[4] - Holdings[j][4]  
                                while(SharesToBePurchased*i[2] > Liquidity):
                                    SharesToBePurchased -=1
                                if((Liquidity - SharesToBePurchased*i[2]) >= 0):
                                    Liquidity -= SharesToBePurchased*i[2] # times by open price
                                    Holdings[j][2] = i[2]
                                    Holdings[j][4] += SharesToBePurchased
                                    Holdings[j][5] = Holdings[j][2]*Holdings[j][4]  
                                    POSREBAL += 1
                                    POSREBALVAL += SharesToBePurchased*Holdings[j][2]
            '''----------------------------Entering New Positions------------------------'''                                
# ENTERING NEW POSITIONS: IF THERE ARE ANY FUNDS STILL AVALIABLE, BUY 
# NEW POSITIONS FROM TOP OF LIST.
        if Trade: 
            newPos = True 
            posList = [] 
            if(Liquidity > 0): 
                for i in SuggestedPos: 
                    posList = [] 
                    for j in Holdings: 
                        if(i[0] == j[0]): 
                            newPos = False
                            posList.append(newPos)
                        else: 
                            if i[0] in QuintTickList:
                                newPos = True
                                posList.append(newPos)
                    if False in posList:
                        pass 
                    else: 
                        list_new = i
                        if(i[2] > Liquidity): # can npt buy one stock 
                            pass 
                        else: 
                            while(list_new[5] > Liquidity): #if position is greater than liquidity or stock price is greater than liquidity 
                                list_new[4] -= 1
                                list_new[5] = int(list_new[4]*list_new[2]) 
                                
                            if(list_new[3] == 'fine'):
                                Holdings.append(list_new)
                                Liquidity -= list_new[5]
                                POSENTERED +=1
                                POSENTEREDVAL += list_new[5]
            else:
                
                pass 
        '''----------------PERFORMANCE MEASURING---------------------------------------
        -------------------------------------------------------------------------------
        ----------------------------------------------------------------------------''' 
        SP500ValList.append(SP500['CLOSE'][index])
        # INVEST A DOLLAR IN INDEX AND DOLLAR IN STRATERGY THEN PLOT RETURNS.
        Holdings_copy = [[row[0]]]
        list_c = []
        PortfolioValue = 0
        for i in Holdings:
            PortfolioValue += i[5]
        PortfolioValue += Liquidity
        
        for i,rows in ticnam.iterrows():
            ticker = rows['Ticker']
            for L,j in zip(Holdings,range(len(Holdings))):
                if L[0] == ticker[2:]:
                    list_c.append(L[0])
                    list_c.append((L[5]/PortfolioValue)*100)
                    list_c.append(ticnam['Name'][i])
                    list_c.append(ticnam['Sector'][i])
                    Holdings_copy.append(list_c)
                    list_c = []                  
        
        HoldingsRecord.write(row[0])
        HoldingsRecord.write("\n")
        HoldingsRecord.write("Trade")
        HoldingsRecord.write(",")
        HoldingsRecord.write(str(Trade))
        HoldingsRecord.write(",")
        HoldingsRecord.write("\n")
        HoldingsRecord.write("Portfolio Value")
        HoldingsRecord.write(",")
        HoldingsRecord.write(str(PortfolioValue))
        HoldingsRecord.write(",")
        HoldingsRecord.write("\n")
        HoldingsRecord.write("Liquidity")
        HoldingsRecord.write(",")
        HoldingsRecord.write(str(Liquidity)) 
        HoldingsRecord.write(",")
        HoldingsRecord.write("\n")
        HoldingsRecord.write("POSentered::")
        HoldingsRecord.write(",")
        HoldingsRecord.write(str(POSENTERED))
        HoldingsRecord.write(",")
        HoldingsRecord.write(str(POSENTEREDVAL))
        HoldingsRecord.write("\n")
        HoldingsRecord.write("Posrebal::")
        HoldingsRecord.write(",")
        HoldingsRecord.write(str(POSREBAL))
        HoldingsRecord.write(",")
        HoldingsRecord.write(str(POSREBALVAL))
        HoldingsRecord.write("\n")
        HoldingsRecord.write("OutOfQuint::")
        HoldingsRecord.write(",")
        HoldingsRecord.write(str(SELLQUINT))
        HoldingsRecord.write(",")
        HoldingsRecord.write(str(SELLQUINTVAL))
        HoldingsRecord.write("\n")
        HoldingsRecord.write("Below100MA::")
        HoldingsRecord.write(",")
        HoldingsRecord.write(str(SELLMA))
        HoldingsRecord.write(",")
        HoldingsRecord.write(str(SELLBEL100MA))
        HoldingsRecord.write("\n")
        HoldingsRecord.write("Negrebal::")
        HoldingsRecord.write(",")
        HoldingsRecord.write(str(NEGREBAL))
        HoldingsRecord.write(",")
        HoldingsRecord.write(str(NEGREBALVAL))
        HoldingsRecord.write("\n")
        
        for j in Holdings_copy[1:]:
            for i in j:
                HoldingsRecord.write(str(i))
                HoldingsRecord.write(",")
            HoldingsRecord.write("\n")
        HoldingsRecord.write("\n")
        DiffList = []
        TFList = []
        for i in SuggestedPos: 
            for j in Holdings: 
                if i[0] == j[0]:
                    TFList.append(True)
                else: 
                    TFList.append(False)
            if True not in TFList: 
                DiffList.append(i)
            TFList = []
            
        print("\n\n")
        print("Date::",row[0])
        print("TRADE" ,Trade, "Liquidity", Liquidity, "Portfolio Value",PortfolioValue,"Num Holdings::",len(Holdings))
        print("POSentered::",POSENTERED , POSENTEREDVAL)
        print("Negrebal::", NEGREBAL, NEGREBALVAL)
        print("Posrebal::",POSREBAL, POSREBALVAL)
        print("OutOfQuint::", SELLQUINT, SELLQUINTVAL)
        print("difference (should be 0)", (PrevLiquidity + NEGREBALVAL + SELLQUINTVAL + SELLBEL100MA - POSREBALVAL - POSENTEREDVAL - Liquidity))
        print("CASH",Liquidity, "POSITIONS IN SUGGPOS", DiffList) 
    else:
        PortfolioValSeries['value'][index] = Liquidity
        pass
    '''-----------RECORDING MONTHLY AND ANUAL RETURNS ---------'''
    if B:    
        PortfolioValue = 0
        if len(Holdings) > 0:
            for i in Holdings:
                PortfolioValue += i[5]
        PortfolioValue += Liquidity
        
        SP500ValList.append(SP500['CLOSE'][index])
        PortfolioValSeries['value'][index] = PortfolioValue
            
        if row[0][-7:-5] != Month: #end of month 
            EndMonth = PortfolioValSeries['value'][(index-1)]
            df[M][Year] = ((EndMonth - StartMonth)/ StartMonth)*100
            print(EndMonth,StartMonth)
            print(df)
            Month = row[0][-7:-5]
            StartMonth = PortfolioValSeries['value'][(index)]
                
        if int(row[0][-4:]) != Year: 
            EndYear = PortfolioValSeries['value'][(index-1)]
            df['Anual'][Year] = ((EndYear - StartYear)/ StartYear)*100
            print(df)
            Year = int(row[0][-4:])
            StartYear = PortfolioValSeries['value'][(index)] 
            StartMonth = PortfolioValSeries['value'][(index)]
            
        if row[0][:2] == '1/': # start of the month 
            StartMonth = PortfolioValSeries['value'][(index)]
            
        if Month == '01':
            M ='Jan'
        elif Month == '02': 
            M ='Feb'            
        elif Month == '03':
            M ='Mar'            
        elif Month == '04':
            M ='Apr'            
        elif Month == '05':
            M ='May'            
        elif Month == '06':
            M ='Jun'            
        elif Month == '07':
            M ='Jul'            
        elif Month == '08':
            M ='Aug'            
        elif Month == '09':
            M ='Sep'            
        elif Month == '10':
            M ='Oct'            
        elif Month == '11':
            M ='Nov'            
        elif Month == '12':
            M ='Dec' 
            
    POSENTERED = 0
    POSENTEREDVAL = 0
    NEGREBAL = 0
    NEGREBALVAL =0
    POSREBAL = 0
    POSREBALVAL = 0
    SELLQUINT = 0
    SELLQUINTVAL = 0
    SELLMA = 0 
    SELLBEL100MA = 0
  