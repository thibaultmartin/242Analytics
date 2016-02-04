from bs4 import BeautifulSoup
import re

# Open file and load it in BeautifulSoup
with open('google10k.html', 'r') as file:
	raw = file.read()
	soup = BeautifulSoup(raw, "html.parser")

	file.close()

links_to_section = {'balance_sheets':'s6664394A37BCC94C11C8A63581ED820F', 'statements_income': 's5C85DE759405741EE2E0A63582A37D42', 'comprehensive_income': 's3E1D1C233561902FF3D5A635820610B0', 'equity': 's2E26AE3C4FD9099BE882A63582176118', 'cash_flows':'s300E7F6ABB5243E137A8A63584CB3357'}

def extract_section(name, links_to_section, soup, columns):
    link = links_to_section[name]

    node = soup.find('a', {"name" : link}).next_sibling.next_sibling.div
    
    print(node)

    #Find the table
    found_table = False
    table = 0
    while not found_table:
        next_node = node.next_sibling
        table = next_node.table
        if table:
            found_table = True
        node = next_node

    # Retrieve Table content
    table = table.tbody
    dic = {}
    key=''
    value=[]
    i=0
    k=0
    for line in table.findAll('tr'):
        for column in line.findAll('td'):
            texte=column.text.encode('utf-8').strip('$')
            key_=re.search('[A-Z]',texte)
            if key_:
                key=texte                
                if key in dic.keys():
                    key=texte+'_'+str(k)
                value={}
                i=0
                k=k+1
            else:
                #Finding the next number                
                figure=re.search('[0-9]',texte)                
                #Displaying a minus sign instead of '('
                texte=re.sub(re.escape('('),'-', texte)
                if figure:
                    value[columns[i]]=texte
                    dic[key]=value
                    i=i+1    
    return(dic)


#%%Different code for equity

def extract_section_equity(name, links_to_section, soup, columns):
    link = links_to_section[name]

    node = soup.find('a', {"name" : link}).next_sibling.next_sibling.div
    
    print(node)

    #Find the table
    found_table = False
    table = 0
    while not found_table:
        next_node = node.next_sibling
        table = next_node.table
        if table:
            found_table = True
        node = next_node

    # Retrieve Table content
    table = table.tbody
    dic = {}
    key=''
    value=[]
    k=0
    for line in table.findAll('tr'):
        for column in line.findAll('td'):
            texte=column.text.encode('utf-8').strip('$')
            key_=re.search('[A-Z]',texte)
            if key_:
                key=texte                
                if key in dic.keys():
                    key=texte+'_'+str(k)
                value=[]
                k=k+1
            else:
                #Finding the next number                
                figure=re.search('[0-9]',texte)                
                #Displaying a minus sign instead of '('
                texte=re.sub(re.escape('('),'-', texte)
                if figure:
                    value.append(texte)
                    dic[key]=value
                    
    for key in dic.keys():
        val={}
        if len(dic[key])==5:
            inside=dic[key]
            for k in range(len(columns)):
                val[columns[k]]=inside[k]
            dic[key]=val
        else:
            inside=dic[key]
            for k in range(len(columns)-1):
                val[columns[k+1]]=inside[k] 
            dic[key]=val
    return(dic)

#%%Extracting income

col_2=[2013,2014]
col_3=[2012,2013,2014]
col_equity=['Shares','Amount','Accumulated Other Comprehensive Income','Retained Earnings','Total Stakeholder Equity']

income=extract_section('statements_income', links_to_section, soup, col_3)
comprehensive=extract_section('comprehensive_income', links_to_section, soup, col_3)
cashflows=extract_section('cash_flows', links_to_section, soup, col_3)
balance=extract_section('balance_sheets', links_to_section, soup, col_2)
equity=extract_section_equity('equity', links_to_section, soup, col_equity)
   
   