# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 21:51:53 2016

@author: Thibault
"""

import pandas as pd
import os
import re
import numpy as np
from bs4 import BeautifulSoup
import Scraper as scraper
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.metrics import *
from nltk.classify import NaiveBayesClassifier as NB
from nltk import word_tokenize, FreqDist,classify, ConditionalFreqDist, pos_tag
from nltk.collocations import BigramCollocationFinder

import collections
import itertools

sector_code='15'

#Importing the list of files from the zip
file_list=pd.read_table('sec.list.txt',sep='_',header=None)
file_list[2]=file_list[2].astype(int).astype(str)


#Importing the list of company names from SEC that correspond to our sector
tic_table=pd.read_table('tic_company_gics.txt')
tic_code=tic_table[tic_table.gsector==int(sector_code)]
tic_code=tic_code.drop_duplicates()

#tic_code['tic'].to_csv('list_of_companies_sector_15.csv',index=False)



#Computing the RoE
ratios=pd.read_csv('selected_companies_ratios.csv',header=False)


ratios['RoE']=ratios['oiadp']*ratios['ceq']
ratios['Net_Profit_Margin']=ratios['oiadp']/ratios['sale']
ratios['Asset_turnover']=ratios['sale']/ratios['at']
ratios['Financial_leverage']=ratios['at']/ratios['ceq']


#%% Matching with the list of files

def file_naming(df):
    return str(df['tic'])+'_'+str(df['datadate'])[0:4]+'-'+str(df['datadate'])[4:6]+'-'+str(df['datadate'])[6:]+'.txt'

ratios['filename']=ratios.apply(file_naming,1)



ratios.to_csv('list_of_companies_sector_15_with_ratios.csv',index=False)

#%% Matching text files with list of files


from os import listdir
from os.path import isfile, join
mypath='files/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

filelist=pd.DataFrame(onlyfiles)
filelist.columns=['filename']

file_with_texts=pd.merge(left=filelist,right=ratios,left_on='filename', right_on='filename')

#%% Retrieving the MD&A

def extract_MDA(df):
    # Credits for the scraper package go to GROUP 7
    mda_text = ''
    with open('files/' + df['filename']) as file:
        soup = BeautifulSoup(file, "lxml")
        
        # We first try the scrape by regex method
        try:
            mda_text = scraper.scrapeByRegex(soup)
            if mda_text:
                mda_text = BeautifulSoup(mda_text, "html.parser").get_text()
                mda_text = re.sub('[^\w]', ' ', mda_text)
                mda_text = re.sub("\d+","",mda_text)
                return mda_text
        except:
            pass

        # We then try the scrapeByAnchorTag method if the previous method didn;t work
        try:
            mda_text = scraper.scrapeByAnchorTag(soup)
            if mda_text:
                mda_text = BeautifulSoup(mda_text, "html.parser").get_text()
                mda_text = re.sub('[^\w]', ' ', mda_text)
                mda_text = re.sub("\d+","",mda_text)
                return mda_text
        except:
            pass

file_with_texts['MDA']=file_with_texts.apply(extract_MDA,1)
