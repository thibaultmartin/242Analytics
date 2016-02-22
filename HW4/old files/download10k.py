# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 00:33:37 2016

@author: martingouy
"""
from bs4 import BeautifulSoup
import requests
import os
#%% Get 10K
def create_document_list(data, count):
    # parse fetched data using beatifulsoup
    soup = BeautifulSoup(data)
    # store the link in the list
    link_list = list()

    # If the link is .htm convert it to .html
    for link in soup.find_all('filinghref')[:count - 1]:
        url = link.string
        if link.string.split(".")[len(link.string.split("."))-1] == "htm":
            url += "l"
        link_list.append(url)
    link_list_final = link_list

    print ("Number of files to download {0}".format(len(link_list_final)))
    print ("Starting download....")

    # List of url to the text documents
    doc_list = list()
    # List of document names
    doc_name_list = list()

    # Get all the doc
    for k in range(len(link_list_final)):
        required_url = link_list_final[k].replace('-index.html', '')
        txtdoc = required_url + ".txt"
        docname = txtdoc.split("/")[-1]
        doc_list.append(txtdoc)
        doc_name_list.append(docname)
    return doc_list, doc_name_list
    
def save_in_directory(doc_list,doc_name_list, company_code):
    # Save every text document into its respective folder
    for j in range(len(doc_list)):
        base_url = doc_list[j]
        r = requests.get(base_url)
        data = r.text
        path = os.path.dirname(os.path.abspath('__file__'))
        print(path)
        with open(os.path.join(path,'downloads/'+company_code+'_'+doc_name_list[j]), "a+") as f:
            f.write(data.encode('ascii', 'ignore'))
                
def filing_10K(company_code, priorto, count):

    # generate the url to crawl
    base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(company_code)+"&type=10-K&dateb="+str(priorto)+"&owner=exclude&output=xml&count="+str(count)
    print ("started 10-K " + str(company_code))

    r = requests.get(base_url)
    data = r.text

    # get doc list data
    doc_list, doc_name_list = create_document_list(data, count)

    try:
        save_in_directory(doc_list, doc_name_list, company_code)
    except Exception,e:
        print str(e)

    print "Successfully downloaded all the files"