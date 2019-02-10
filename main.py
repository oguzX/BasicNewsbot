import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.haberler.com/')
source = BeautifulSoup(r.content, "lxml")

source.decode("utf-8")
data = source.select(".second-news a[title]")

for x in data:
    print(x["title"])
