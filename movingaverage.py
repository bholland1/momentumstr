# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 19:14:49 2017

@author: brock
"""

import numpy as np

def moving_average(seq, wsize):
    count = 0
    moving_avg = np.array([])    
    
    for i in seq:
        if count < (wsize-1):
            count += 1
            pass
        else:
           m = (np.sum(seq[(count+1 - wsize): count+1]))/wsize
           print(m)
           moving_avg = np.append(moving_avg, m, axis = None)
           count += 1
    return moving_avg

