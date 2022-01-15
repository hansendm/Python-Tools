# pip install google
from googlesearch import search
query = "digitalnote.org"
 
for url in search(query):
    print(url)
