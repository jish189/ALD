from pybliometrics.scopus import AbstractRetrieval, AuthorRetrieval, CitationOverview, ScopusSearch
import pandas as pd

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
