# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 17:27:02 2017

@author: brock
"""
import pickle
import bs4 as bs
import requests

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    tickers[tickers.index('BRK.B')] = 'BRK-B'
    tickers[tickers.index('BF.B')] = 'BF-B'
    
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
    return tickers