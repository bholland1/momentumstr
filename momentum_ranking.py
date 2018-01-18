# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 17:49:16 2017

@author: brock

// --------------------------------------------------------------------
//
// Major Functions:	Momentum ranking 
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
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
import statsmodels.api as sm
import numpy as np
import seaborn as sns


def momentum_ranking(ticker):      
    #print(ticker)
    ticker.head().round(2)
    ticker['Log'] =  np.log(ticker['CLOSE'])
    ticker['Index'] = range(len(ticker))
    model = smf.ols(formula = "ticker['Log'] ~ ticker['Index']", data = ticker) 
    results = model.fit()
    R = results.rsquared
    slope = results.params[1]
    ann_slope = ((1 + slope)**252) - 1
    adj_slope = ann_slope * R
    return (adj_slope)