# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 17:58:00 2017

@author: brock
// --------------------------------------------------------------------
//
// Major Functions:	List Final 
//
// --------------------------------------------------------------------
//
// Revision History :
// --------------------------------------------------------------------
//   Ver  :| Author            :| Mod. Date :| Changes Made:
//   V1.0 :| Brock             :| 03/25/2010:| Initial Revision

// --------------------------------------------------------------------
"""
from Ranker import ranker
from allocation import allocation


def list_final(Rank_list, ATR_period, risk_factor, funds_available):
    '''
    Returns a final list with ticker, adj. slope, open price, allocation of shares and total
    funds allocated to the share.
    Format will appear as follows:
    [(company ticker), (adj. slope), (current open price),  (shares), (funds allocated)]
    
    '''
    final_list = [] 
    i_list = []
    funds_allocated = 0
    liquidity = funds_available
     
    for i in Rank_list:
        print(i)
        liquidity -= funds_allocated 
        funds_allocated = 0
    
        shares = allocation(i[0], ATR_period, risk_factor, funds_available)
        funds_allocated = shares * i[2]
    
        
        if funds_allocated > liquidity:
            shares = int(liquidity/i[2])
            funds_allocated = shares * i[2]
            i_list.append(i)
            i_list.append(shares)            
            i_list.append(funds_allocated)
            final_list.append(i_list)
            i_list = []
            return final_list
            
        else:
            i_list.append(i)
            i_list.append(shares)            
            i_list.append(funds_allocated)
            final_list.append(i_list)
            i_list = []