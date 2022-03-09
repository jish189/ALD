from pybliometrics.scopus import AbstractRetrieval, AuthorRetrieval, CitationOverview, ScopusSearch
import pandas as pd

# downward references are stored in the ab object.
# how to get upward references? the link to those results is given by ab.citedby_link
# query for scp value from citedby_link!

# doi = "10.1088/0022-3727/42/7/073001"
# ab = AbstractRetrieval(doi, view='FULL')
# print(ab.citedby_link)
#
# id = ab.eidd
# file = ScopusSearch('63649098537')

doi = '10.1021/acs.chemmater.5b00255'
ab = AbstractRetrieval(doi, view='FULL')
print(ab.authors)
for author in ab.authors:
    print(author.indexed_name)
# from urllib.parse import urlparse
# print(urlparse(ab.citedby_link, allow_fragments=True))
citation_query = ab.citedby_link.split('&')[-2].split('=')[1]
print(citation_query)
file = ScopusSearch(citation_query)
# print(file)
for item in file.results:
    print(item.eid)

# reference_term = ab.citedby_link[]
# id = ab.eid
print(file.results)

# import urllib.request
# from urllib.error import HTTPError
#
# url = ab.citedby_link
# req = urllib.request.Request(url)
#
# cited_by=''
# print(req.get_header())
#
# with urllib.request.urlopen(req) as f:
#     cited_by = f.read().decode()
#
# with open('cited_by.txt', 'w') as writefile:
#     writefile.write(cited_by)
# #
# # # # # citedby api does not work...
# # #
# # # # https://www.scopus.com/search/submit/citedby.uri?eid=2-s2.0-63649098537
# # #
# # #
# # # pub_year = int(ab.coverDate.split('-')[0])
# # # # print(pub_year)
# # # co = CitationOverview(id, start=pub_year)