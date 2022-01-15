# pip install requests
#method 1
import urllib.request
from urllib.request import Request, urlopen
req = Request('https://digitalnote.org', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).getcode()
print(webpage) # 200
# method 2
import requests
r = requests.get("https://digitalnote.org")
print(r.status_code) # 200
