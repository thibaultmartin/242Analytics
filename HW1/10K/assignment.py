from bs4 import BeautifulSoup
import re
import nltk
from matplotlib import pyplot as plt

nltk.download('punkt')


def word_count(filename,term):
	with open(filename, 'r') as file:
		report = file.read()

		soup = BeautifulSoup(report, "html.parser")
		text = soup.getText().lower()
		words = nltk.word_tokenize(text)
		fd = nltk.FreqDist(words)
		return(float(fd[term]) / len(words))
		#return((float(fd['increase']) + float(fd['growth']) + float(fd['improve']) + float(fd['expand']))/ len(words))

results = {'Microsoft':[], 'apple': [], 'gm': []}
years = ['2013', '2014', '2015']

def frequency(term):
    for key in results.keys():
        for year in years:
		results[key].append(word_count('/Users/Thibault/Documents/Boulot/UC Berkeley/IEOR242/HW1/10K/10K/{}-{}.html'.format(key, year),term))

results = {'Microsoft':[], 'apple': [], 'gm': []}
frequency('growth')

results = {'Microsoft':[], 'apple': [], 'gm': []}
frequency('improve')

results = {'Microsoft':[], 'apple': [], 'gm': []}
frequency('higher')

results = {'Microsoft':[], 'apple': [], 'gm': []}
frequency('unexpected')

results = {'Microsoft':[], 'apple': [], 'gm': []}
frequency('expansion')

results = {'Microsoft':[], 'apple': [], 'gm': []}
frequency('innovation')

print(results)

plt.plot([2013,2014,2015], results['Microsoft'], [2013,2014,2015], results['apple'], [2013,2014,2015], results['gm'])
plt.ylabel = 'Frequency of positive words'
plt.show()


#%% Idibon Free API

import httplib
import json

def main():
# Establishes an HTTP connection with the local Idibon Public server
    connection = httplib.HTTPConnection("localhost:8080")

# Enter the content you want to send to the Idibon Public server below
    your_content = "Your content goes here."
    body = json.dumps({"content": your_content})

# Sends a GET request to the server for the English Social Sentiment model
    connection.request("GET", "/Idibon/EnglishSocialSentiment", body)
    response = connection.getresponse()
    res = response.read()

# Formats the prediction from the Idibon Public server to print
    json_res = json.loads(res[1:-1])
    print json.dumps(json_res, sort_keys = True, indent = 4, separators = (',', ': '))

# Closes the HTTP connection
    connection.close()

    return

main()
