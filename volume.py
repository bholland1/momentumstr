# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 16:07:08 2017

@author: Aaron
"""

import pandas as pd
import csv
import numpy as np
from zigzag import zigzag
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from datetime import datetime

def ordvolume(file, swing):
    
    count_start = 0
    count_end = 1
    s_slist = []
    s_object = []
    timeseries = pd.read_csv(file)
    timeseries['Index']=timeseries.index
    timeseries['Date']=pd.to_datetime(timeseries['Unnamed: 0'])

    series = zigzag(timeseries, pct=swing)
    series['Index']=series.index    
    
    for i in series:
        if count_end == (len(series)-1):
            return s_object
        else:       
            swing_obj = (timeseries['Index'] >= series['Index'][count_start] ) & (timeseries['Index'] <= series['Index'][count_end])
            df = timeseries.loc[swing_obj]
            count_start += 1
            count_end += 1
            avg_vol = df['VOL'].mean()
            swing_mov = (df['CLOSE'].iloc[-1] - df['CLOSE'].iloc[0])/(df['CLOSE'].iloc[0])
            s_list = [df['Date'].iloc[0], df['Date'].iloc[-1], 'Avg vol:', avg_vol, 'Price movement:', swing_mov]
            s_object.append(s_list)
            
    return s_object

    
'''
Ideas:

- Seperate average up and down day volume in periods?

'''
def ord_plot(file,s_object): 
    timeseries = pd.read_csv(file)
    timeseries['Date']=pd.to_datetime(timeseries['Unnamed: 0'])
    
    Time_list = list(timeseries['Date'])
    
    PricePts = []
    DatePts  = []
    Vol = []
    A = True
    for index in s_object: 
        if(A):
            I = Time_list.index(index[0])
            J = Time_list.index(index[1])
            A = False
            if(type(timeseries['CLOSE'][I]) == None):
                I -= 1
            if(type(timeseries['CLOSE'][J]) == None):
                J -= 1
            PricePts.append(timeseries['CLOSE'][I])
            PricePts.append(timeseries['CLOSE'][J])
            DatePts.append(timeseries['Date'][I])
            DatePts.append(timeseries['Date'][J])
        else:
             J = Time_list.index(index[1])
             if(type(timeseries['CLOSE'][J]) == None):
                 J -= 1
             PricePts.append(timeseries['CLOSE'][J])
             DatePts.append(timeseries['Date'][J])
        Vol.append(index[3])
    DatePts = [pd.datetime.date(i) for i in DatePts]

    return PricePts, DatePts, Vol



timeseries = pd.read_csv('HAL.csv')
timeseries['Index']=timeseries.index
timeseries['Date']=pd.to_datetime(timeseries['Unnamed: 0'])

S = ordvolume('HAL.csv', 20)
PricePts, DatePts, Vol = ord_plot('HAL.csv',S)
fig = plt.figure(figsize=(100,100))
ax = fig.add_subplot(111)
ax.plot(DatePts,PricePts,'r')
ax.hold
ax.plot(timeseries['Date'],timeseries['CLOSE'])

interDate = []
interPrice =[]

Vol = [round(n,2) for n in Vol]

i = 0
while i != (len(DatePts)-1): 
    interPrice.append((PricePts[i] + PricePts[i+1])/2)
    interDate.append((DatePts[i]+(DatePts[i+1] - DatePts[i])/2))
    i += 1
    
   
for i,j,k in zip(interDate, interPrice, Vol):
    ax.annotate(str(k), xy=(i,j))
    
