from pybliometrics.scopus import AbstractRetrieval, AuthorRetrieval, CitationOverview, ScopusSearch
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


def SentenceLoc(string, keyword, delimiter = '. '):
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
'''
doi = "10.1088/0022-3727/42/7/073001"

# ab = AbstractRetrieval(doi,)
# id = ab.eid
# print(ab.citedby_link)

search = ScopusSearch('"Atomic Layer Deposition" AND "Quadrupole Mass Spectrometry"', verbose=True)

df = pd.DataFrame(pd.DataFrame(search.results))
total_words = 0
for id in df.eid:
    ab = AbstractRetrieval(id)
    # print (type(ab.description))
    abstract_length = len(str(ab.description).split(' '))
    total_words += abstract_length

print(total_words)
# # citedby api does not work...

# https://www.scopus.com/search/submit/citedby.uri?eid=2-s2.0-63649098537


# pub_year = int(ab.coverDate.split('-')[0])
# print(pub_year)
# co = CitationOverview(id, start=pub_year)
'''


if __name__ == '__main__':
    fulltext = SimpleTextRetrieval(id, DOI = False)
    outputs = SentenceLoc(fulltext, 'GPC')
    with open('test.txt', 'w') as f:
        f.write(outputs)