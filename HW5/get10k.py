# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 14:57:38 2016

@author: Thibault
"""

#%%
import re
from SECEdgar.crawler import SecCrawler
#%% GEt names of companies

sector_code = '15'

list_companies = []
with open('tic_company_gics.txt') as file:
    for line in file:
        sector = line[-3:-1]
        if sector == sector_code:
            name_company = re.search('[\w\.]+', line).group()#[:-1]
            list_companies.append(name_company)
            
list_companies=list(set(list_companies))
        

        
#%%  Download the 10K
number_of_companies = 200
date_retrieve = '20160101'
number_10K = 10

secCrawler = SecCrawler()

for company in list_companies[0:number_of_companies]:
    secCrawler.filing_10K(company, date_retrieve, number_10K)
    

#%%   Doing the 'matching' to find the proper file names
 
import pandas as pd

#Importing the list of files from the zip
file_list=pd.read_table('sec.list.txt',sep='_',header=None)
file_list[2]=file_list[2].astype(int).astype(str)


#Importing the list of company names from SEC that correspond to our sector
tic_table=pd.read_table('tic_company_gics.txt')
tic_code=tic_table[tic_table.gsector==int(sector_code)]
tic_code=tic_code.drop_duplicates()


#Merging those and retrieving the useful links
merged_docs=pd.merge(tic_code,file_list,how='left',left_on='conm',right_on=3)

merged_docs.columns=['tic','conm','gsector','0','1','2','3','4','5']
merged_docs=merged_docs[merged_docs['2'].notnull()]
merged_docs['link'] = merged_docs[['0','1','2','3','4','5']].apply(lambda x: '_'.join(x), axis=1)


relevant_indexes=list(set(merged_docs['2']))


#RETRIEVING THE RIGHT FILES THE RIGHT LIST (WITH NAME CHANGES)
file_list3=file_list[file_list[2].isin(relevant_indexes)]

list_of_links = list(file_list3[[0,1,2,3,4,5]].apply(lambda x: '_'.join(x), axis=1))

print(list_of_links)





