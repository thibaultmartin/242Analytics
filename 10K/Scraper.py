# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 2016
Author: chongwee
Modified by Cedric Vallee Feb 29 2016
"""

import regex #pip install regex, needed for the overlapping flag
import re

def scrapeByRegex(soup):

    text = ''.join(soup.findAll(text=True))

    text.replace("&#146;","'")
    
    regexp = regex.compile(r'Item[\r\n\s]*\d\s*[:|.|-]*[\r\n\s]*Management\S*s[\r\n\s]*Discussion.*Item[\r\n\s]*\d\s*[:|.|-]*[\r\n\s]*\w*[\r\n\s]*Financial[\r\n\s]*Statements', regex.MULTILINE|regex.DOTALL|regex.IGNORECASE|regex.UNICODE)
        
    matches = regex.findall(regexp,text,overlapped=True)
    
    if len(matches) == 0: 
        return None                
        
    if len(matches[-1]) < 250: #ensure that the scraped text is sufficiently long.
        return None
        
    return matches[-1]


def scrapeByAnchorTag(soup):
    
    fullText = ""

    #find location of Items 7 and 8 from the links in the table of content
    item7tag = soup.find('a', href=True, text=re.compile('Discussion and Analysis of Financial Condition'))
    if item7tag is None:
        return None
    item7href = item7tag['href']
    if item7href.startswith('#'):
       item7href = item7href.replace('#','')         
    item8tag = soup.find('a', href=True, text=re.compile('Financial Statements and Supplementary Data'))
    if item8tag is None:
        return None
    item8href = item8tag['href']        
    if item8href.startswith('#'):
       item8href = item8href.replace('#','')                        
    
    #locate the tag indicating the start of Item 7
    currentTag = soup.find('a', {"name":item7href})

    #loop through the subsequent tags until we hit Item 8
    while True and currentTag is not None:
        
        if currentTag.name == 'font':
            
            #extract the text
            currentStr =  ''            
            for s in currentTag.strings:
                currentStr = '{0} {1}'.format(currentStr, s).strip()

            fullText = '{0} {1}'.format(fullText, currentStr)
        
        #check whether we've reached Item 8. Stop parsing document if so               
        if currentTag.name == 'a':
            if currentTag.has_attr('name'):
                if currentTag['name'] == item8href:
                    break
        
        #move on to the next tag            
        currentTag = currentTag.find_next(['font','a'])
        
        #if we reach this point, it means that the code did not locate Item 8            
        if currentTag is None:
            return None
    
    if len(fullText) < 250: #ensure that the scraped text is sufficiently long.
        return None
    
    return fullText            
            