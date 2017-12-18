# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 15:21:56 2017

@author: Aaron
"""
from __future__ import division

from functools import wraps

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from pandas.stats import moments
 
def zigzag(s, pct=5):
        
    #s = pd.read_csv(s) 
    ut = 1 + pct / 100
    dt = 1 - pct / 100

    ld = s.index[0]
    lp = s.CLOSE[ld]
    tr = None

    zzd, zzp = [ld], [lp]

    for ix, ch, cl in zip(s.index, s.HIGH, s.LOW):
        # No initial trend
        if tr is None:
            if ch / lp > ut:
                tr = 1
            elif cl / lp < dt:
                tr = -1
        # Trend is up
        elif tr == 1:
            # New high
            if ch > lp:
                ld, lp = ix, ch
            # Reversal
            elif cl / lp < dt:
                zzd.append(ld)
                zzp.append(lp)

                tr, ld, lp = -1, ix, cl
        # Trend is down
        else:
            # New low
            if cl < lp:
                ld, lp = ix, cl
            # Reversal
            elif ch / lp > ut:
                zzd.append(ld)
                zzp.append(lp)

                tr, ld, lp = 1, ix, ch

    # Extrapolate the current trend
    if zzd[-1] != s.index[-1]:
        zzd.append(s.index[-1])

        if tr is None:
            zzp.append(s.CLOSE[zzd[-1]])
        elif tr == 1:
            zzp.append(s.HIGH[zzd[-1]])
        else:
            zzp.append(s.LOW[zzd[-1]])

    return Series(zzp, index=zzd)