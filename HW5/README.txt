Please uninstall any version of the SECEdgar library:

"pip unistall SECEdgar"

Install this new version:
"pip install git+https://github.com/martingouy/SEC-Edgar"


Explanation of the code:

Lines 1-37: downloads all 10-K files from a number of companies that we are interested in.
This method uses the updated library downloaded as shown above.

Inputs: ‘number of 10-K files’, ‘Latest date of documents (retrieve docs before …)’, ‘number of companies’ from the list.




2nd part: Matching

We implemented a version of the matching, retrieving the list of all the links to the documents in the zip file that correspond to our sector.

To deal with the changes in names, etc, we did the following:

1. Extract the names of the companies of our sector from the GICS file
2. For each of these companies, find their unique identifier in the link in the zip file (a multiple digit code just after the Q1/2/3/4 in the link for each company)
3. Retrieve a subset of the sec list of docs in the zip, taking only those that correspond to these unique identifiers.

For instance, take Apple Inc. We find its ‘code’ in the document file (sec.list.txt) which could be 12345. Then we retrieve in the SEC file (sec.list.txt) all the links that have 12345 as ‘unique identifiers’, which thus correspond to ‘Apple Inc.’, but also ‘Apple Computer Inc’, etc.

There is no need for stemming/regex, and we are sure to get the right links, and all of them.