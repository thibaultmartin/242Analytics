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

#ratios.to_csv('list_of_companies_sector_15_with_new_ratios.csv',index=False)


#%%Counting the changes in ratios
data=ratios

n = len(data)
data['d_RoE'] = np.zeros(n)
data['d_Net_Profit_Margin'] = np.zeros(n)
data['d_Asset_turnover'] = np.zeros(n)
data['d_Financial_leverage'] = np.zeros(n)


count = 0
gvkey = ''
for i, row in data.iterrows():
    if row['gvkey'] != gvkey:
        count += 1
        gvkey = row['gvkey']
    else:
        last_row = data.iloc[i - 1, :]
        if row['fyear'] - last_row['fyear'] == 1:
            data.loc[i,'d_RoE'] = row['RoE'] - last_row['RoE']
            data.loc[i,'d_Net_Profit_Margin'] = row['Net_Profit_Margin'] - last_row['Net_Profit_Margin']
            data.loc[i,'d_Asset_turnover'] = row['Asset_turnover'] - last_row['Asset_turnover']
            data.loc[i,'d_Financial_leverage'] = row['Financial_leverage'] - last_row['Financial_leverage']



#%% Matching text files with list of files


from os import listdir
from os.path import isfile, join
mypath='files/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

filelist=pd.DataFrame(onlyfiles)
filelist.columns=['filename']

file_with_texts=pd.merge(left=filelist,right=data,left_on='filename', right_on='filename')

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



#%% Creating the dataframe for MultinomialNB

def ispositive_delta_RoE(df):
    if df['d_RoE']>0:
        return 1
    elif df['d_RoE']==0:
        return 'N/A'
    else:
        return 0

def ispositive_d_Net_Profit_Margin(df):
    if df['d_Net_Profit_Margin']>0:
        return 1
    elif df['d_Net_Profit_Margin']==0:
        return 'N/A'
    else:
        return 0

def ispositive_d_Asset_turnover(df):
    if df['d_Asset_turnover']>0:
        return 1
    elif df['d_Asset_turnover']==0:
        return 'N/A'
    else:
        return 0

def ispositive_d_Financial_leverage(df):
    if df['d_Financial_leverage']>0:
        return 1
    elif df['d_Financial_leverage']==0:
        return 'N/A'
    else:
        return 0

print(dataset.columns)
dataset=pd.read_csv('final.csv', header=False)

#Returns if the document is positive or negative (based on change on RoE)
dataset['d_RoE_pos']=dataset.apply(ispositive_delta_RoE,1)
dataset['d_Asset_turnover_pos']=dataset.apply(ispositive_d_Asset_turnover,1)
dataset['d_Financial_leverage_pos']=dataset.apply(ispositive_d_Financial_leverage,1)
dataset['d_Net_Profit_Margin_pos']=dataset.apply(ispositive_d_Net_Profit_Margin,1)

#dataset.to_csv('final_labeled.csv',index=False)


#%%MultinomialNB

#dataset=pd.read_csv('data_industry.csv',header=False)

dataset=dataset[pd.notnull(dataset['MDA'])]
dataset=dataset[dataset['d_RoE_pos']!='N/A']


# We split the dataset in train/test ratio: 0.30
train_set, test_set = train_test_split(dataset, test_size = 0.30)

# We initiate the classifier
vectorizer = CountVectorizer(stop_words="english")
counts = vectorizer.fit_transform(train_set.MDA.values)
classifier = MultinomialNB(fit_prior="False")


#%%Using d_RoE

# We fit the training set
classifier.fit(counts, train_set.d_RoE_pos.values.astype(int))

# Let's do some prediction on the test set
predictions = classifier.predict(vectorizer.transform(test_set.MDA.values)) 
test_set_pred = pd.Series(predictions, index=test_set.index)

tab = pd.crosstab(test_set.d_RoE_pos, test_set_pred, rownames=['Actual'], colnames=['Predicted'], margins=True) # Print confusion matrix
print(tab)

print "Accuracy: %f" %(np.float(tab[0][0]+tab[1][1])/(tab['All']['All']))
print(classification_report(test_set.d_RoE_pos.astype(int), test_set_pred)) # Print accuracy, precision, recall, F m


#%%Using d_Net_Profit_Margin

# We fit the training set
classifier.fit(counts, train_set.d_Net_Profit_Margin_pos.values.astype(int))

# Let's do some prediction on the test set
predictions = classifier.predict(vectorizer.transform(test_set.MDA.values)) 
test_set_pred = pd.Series(predictions, index=test_set.index)

tab = pd.crosstab(test_set.d_Net_Profit_Margin_pos, test_set_pred, rownames=['Actual'], colnames=['Predicted'], margins=True) # Print confusion matrix
print(tab)

print "Accuracy: %f" %(np.float(tab[0][0]+tab[1][1])/(tab['All']['All']))
print(classification_report(test_set.d_Net_Profit_Margin_pos.astype(int), test_set_pred)) # Print accuracy, precision, recall, F m


#%%Using d_Financial_leverage_pos

# We fit the training set
classifier.fit(counts, train_set.d_Financial_leverage_pos.values.astype(int))

# Let's do some prediction on the test set
predictions = classifier.predict(vectorizer.transform(test_set.MDA.values)) 
test_set_pred = pd.Series(predictions, index=test_set.index)

tab = pd.crosstab(test_set.d_Financial_leverage_pos, test_set_pred, rownames=['Actual'], colnames=['Predicted'], margins=True) # Print confusion matrix
print(tab)

print "Accuracy: %f" %(np.float(tab[0][0]+tab[1][1])/(tab['All']['All']))
print(classification_report(test_set.d_Financial_leverage_pos, test_set_pred)) # Print accuracy, precision, recall, F m


#%%Using d_Asset_turnover_pos

# We fit the training set
classifier.fit(counts, train_set.d_Asset_turnover_pos.values.astype(int))

# Let's do some prediction on the test set
predictions = classifier.predict(vectorizer.transform(test_set.MDA.values)) 
test_set_pred = pd.Series(predictions, index=test_set.index)

tab = pd.crosstab(test_set.d_Asset_turnover_pos, test_set_pred, rownames=['Actual'], colnames=['Predicted'], margins=True) # Print confusion matrix
print(tab)

print "Accuracy: %f" %(np.float(tab[0][0]+tab[1][1])/(tab['All']['All']))
print(classification_report(test_set.d_Asset_turnover_pos.astype(int), test_set_pred)) # Print accuracy, precision, recall, F m



#%%Multinomial by sector
"""Doing the Multinomial Naïve Bayes by industry sectors"""


#dataset=pd.read_csv('data_industry.csv',header=False)

industries=list(set(dataset['gind']))
industries.remove(451020)

def MultiNBclassifier(industry_code, dataset):
    data=dataset[pd.notnull(dataset['MDA'])]
    data=data[data['d_RoE_pos']!='N/A']
    data=data[data['gind']==industry_code]


    # We split the dataset in train/test ratio: 0.30
    train_set, test_set = train_test_split(data, test_size = 0.30)

    # We initiate the classifier
    vectorizer = CountVectorizer(stop_words="english")
    counts = vectorizer.fit_transform(train_set.MDA.values)
    classifier = MultinomialNB(fit_prior="False")

    # We fit the training set
    classifier.fit(counts, train_set.d_RoE_pos.values.astype(int))

    # Let's do some prediction on the test set
    predictions = classifier.predict(vectorizer.transform(test_set.MDA.values)) 
    test_set_pred = pd.Series(predictions, index=test_set.index)

    tab = pd.crosstab(test_set.d_RoE_pos, test_set_pred, rownames=['Actual'], colnames=['Predicted'], margins=True) # Print confusion matrix
    print(tab)

    print "Accuracy: %f" %(np.float(tab[0][0]+tab[1][1])/(tab['All']['All']))
    print(classification_report(test_set.d_RoE_pos.astype(int), test_set_pred))    
    # Print accuracy, precision, recall, F m


#Training and testing the model for each industry
for ind_code in industries:
    print('THE INDUSTRY CODE IS '+str(ind_code))
    MultiNBclassifier(ind_code,dataset)