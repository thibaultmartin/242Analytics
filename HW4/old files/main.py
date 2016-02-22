# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 22:32:13 2016

@author: martingouy
"""
#%%
import pandas as pd
import re
from cPickle import dump
from requests import get
from SECEdgar.crawler import SecCrawler
#%% GEt names of comapnies

sector_code = '10'

def get_cik(name):
    
    URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
    CIK_RE = re.compile(r'.*CIK=(\d{10}).*')
    cik = ''
    results = CIK_RE.findall(get(URL.format(name)).content)
    if len(results):
        cik = str(results[0])
    
    return cik

list_companies = []
with open('tic_company_gics.txt') as file:
    for line in file:
        sector = line[-3:-1]
        if sector == sector_code:
            name_company = re.search('[\w\.]+', line).group()#[:-1]
            list_companies.append(name_company)
            
list_companies = list(set(list(list_companies)))
#%% GEt SIC code for each company
list_companies_cik = []

for company in list_companies:
    cik = get_cik(company)
    if len(cik) > 0:
        list_companies_cik.append((company, cik))
        
#%% Get 10K

secCrawler = SecCrawler()

for name, cik in list_companies_cik:
    secCrawler.filing_10K(name, cik, '20150101', '1')