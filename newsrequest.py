import requests, siteclass
from bs4 import BeautifulSoup


class newsrequest:
    haberlerCom = siteclass.site("Haberler", "https://www.haberler.com/", ".second-news a[title]")
    haber7 = siteclass.site("haberler7", "http://www.haber7.com/", ".subhead-slider a[title]")
    hurriyet = siteclass.site("Hurriyet", "http://www.hurriyet.com.tr/", ".swiper-wrapper a[title]")
    newsSites = []
    newsSites.append(haber7)
    newsSites.append(haberlerCom)
    newsSites.append(hurriyet)

    def getNews(self):
        for siterow in self.newsSites:
            self.drawline(30)
            print(siterow.getsitename())
            r = requests.get(siterow.getsiteurl())
            source = BeautifulSoup(r.content, "lxml")
            data = source.select(siterow.getcontenttarget())
            for x in data:
                if x["title"] != "":
                    print(str(x["title"]).lower())

    def drawline(self, count):
        print('\n')
        for x in range(int(count)):
            print("-",end="")
        print('\n')
