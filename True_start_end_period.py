# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 17:36:19 2017

@author: brock
"""
from pandas.tseries.offsets import BDay
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
import pandas_market_calendars as mcal
import pandas as pd


def True_start_end_period(period, *start_date):
    ##In format --> start_data = 2017/10/30
    nyse = mcal.get_calendar('NYSE')
    period_init = period
    if not start_date:
        start = pd.datetime.today() - BDay(period_init)
        end = pd.datetime.today()
    else:
        start_date = start_date.split('/').split('-')
        start = pd.datetime(start_date[0],start_date[1],start_date[2]) - BDay(period_init)
        end = pd.datetime(start_date[0],start_date[1],start_date[2])
        
    dates = nyse.schedule(start_date=start, end_date=end)
    date_range = mcal.date_range(dates,frequency ='1D')
    ###   
    while(len(date_range) <= period_init):
        start = start - BDay(1)
        end = pd.datetime.today()
        dates = nyse.schedule(start_date=start, end_date=end)
        date_range = mcal.date_range(dates,frequency ='1D')
        
    return start, end