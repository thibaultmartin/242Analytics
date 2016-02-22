# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 22:32:13 2016

@author: martingouy
"""
#%%
import re
from SECEdgar.crawler import SecCrawler
#%% GEt names of companies

sector_code = '10'

list_companies = []
with open('tic_company_gics.txt') as file:
    for line in file:
        sector = line[-3:-1]
        if sector == sector_code:
            name_company = re.search('[\w\.]+', line).group()#[:-1]
            list_companies.append(name_company)
            
list_companies = list(set(list(list_companies)))
        

        
#%%  Download the 10K
number_of_companies = 50
date_retrieve = '20150101'
number_10K = 5

secCrawler = SecCrawler()

for company in list_companies[0:number_of_companies]:
    secCrawler.filing_10K(company, date_retrieve, number_10K)

