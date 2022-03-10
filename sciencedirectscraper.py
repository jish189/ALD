import pandas as pd
import requests
from xml.etree import ElementTree
from nltk import tokenize

key = '6ef00383da752dc9baee869bf9b1b46b'
id = 'S027288422030002X'

def SimpleTextRetrieval(id, DOI=True):
    if DOI:
        query = 'https://api.elsevier.com/content/article/doi/{0}?APIKey={1}&httpAccept=text/plain'.format(id,key)
    else:
        query = 'https://api.elsevier.com/content/article/pii/{0}?APIKey={1}&httpAccept=text/plain'.format(id,key)
    response = requests.get(query)
    
    return(response.text)

def JSONRetrieval(id, DOI=True):
    if DOI:
        query = 'https://api.elsevier.com/content/article/doi/{0}?APIKey={1}'.format(id,key)
    else:
        query = 'https://api.elsevier.com/content/article/pii/{0}?APIKey={1}'.format(id,key)
    
    header = {"Accept": "application/json"}
    
    response = requests.get(query, headers=header)
    abstract = response.json()["full-text-retrieval-response"]['coredata']['dc:description']
    text = response.json()["full-text-retrieval-response"]['originalText']
    
    return(abstract + ' ' + text)

def AbstractRetrieval(id, DOI=True):
    if DOI:
        query = 'https://api.elsevier.com/content/article/doi/{0}?APIKey={1}'.format(id,key)
    else:
        query = 'https://api.elsevier.com/content/article/pii/{0}?APIKey={1}'.format(id,key)
    
    header = {"Accept": "application/json"}
    
    response = requests.get(query, headers=header)
    abstract = response.json()["full-text-retrieval-response"]['coredata']['dc:description']
    
    return(abstract)


def FullTextRetrieval(id, DOI=True):
    if DOI:
        query = 'https://api.elsevier.com/content/article/doi/{0}?APIKey={1}&httpAccept=text/xml'.format(id,key)
    else:
        query = 'https://api.elsevier.com/content/article/pii/{0}?APIKey={1}&httpAccept=text/xml'.format(id,key)
    response = requests.get(query)
    
    tree = ElementTree.fromstring(response.content)

    for child in tree:
        print(child.tag, child.attrib)

    return('hi')

def PutRetrieval(id, DOI=True):



    if DOI:
        query = 'https://api.elsevier.com/content/article/doi/{0}?httpAccept=application/json&APIKey={1}&httpAccept=text/plain'.format(id,key)
    else:
        query = 'https://api.elsevier.com/content/article/pii/{0}?httpAccept=application/json&APIKey={1}&httpAccept=text/plain'.format(id,key)
    response = requests.put(query)
    
    return(response.text)

def SentenceLoc(string, keyword):
    # split string into sentences via delimiter, default period
    # sentences = string.split(delimiter)
    sentences = tokenize.sent_tokenize(string)
    chunks = [] # list of all sentences containing keyword

    for v in sentences:
        if keyword in v:
            chunks.append(v)

    # check all chunks for keywords of length, nm and Å

    chunks = [s for s in chunks if "Å" in s or "nm" in s]

    #return " ".join(chunks)

    #return first instance of GPC, likely to be the sentence to talk about growth rate
    return chunks[0]

if __name__ == '__main__':
    # fulltext = SimpleTextRetrieval(id, DOI = False)
    # outputs = SentenceLoc(fulltext, 'GPC')
    # with open('test.txt', 'w') as f:
    #     f.write(outputs)

    fulltext = JSONRetrieval(id, DOI = False)
    outputs = SentenceLoc(fulltext, 'cycle')

    abst = AbstractRetrieval(id, DOI = False)

    with open('test.txt', 'w') as f:
        f.write(outputs + '\n' + abst)