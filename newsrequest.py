import requests, siteclass
from bs4 import BeautifulSoup
import database, datetime


class newsrequest:
    haberlerCom = siteclass.site("Haberler", "https://www.haberler.com/", ".second-news a[title]")
    haber7 = siteclass.site("haberler7", "http://www.haber7.com/", ".subhead-slider a[title]")
    hurriyet = siteclass.site("Hurriyet", "http://www.hurriyet.com.tr/", ".swiper-wrapper a[title]")
    ensonhaber = siteclass.site("En son haber", "https://www.ensonhaber.com/", ".headline a[title]")
    sozcu = siteclass.site("Sozcu", "https://www.sozcu.com.tr/", ".swiper-wrapper a[title]")
    haberturk = siteclass.site("Haberturk", "https://www.haberturk.com/", ".swiper-wrapper a[title]")
    sondakika = siteclass.site("Son Dakika", "https://www.sondakika.com/", ".bxslider a[title]")
    internethaber = siteclass.site("Internet haber", "https://www.internethaber.com/", ".swiper-wrapper a[title]")
    ntv = siteclass.site("NTV", "https://www.ntv.com.tr/", ".slidee a[title]")
    cnn = siteclass.site("CNN Turk", "https://www.cnnturk.com/haberler/", ".container a[title]")

    newsSites = []
    newsSites.append(haber7)
    newsSites.append(haberlerCom)
    newsSites.append(hurriyet)
    newsSites.append(ensonhaber)
    newsSites.append(sozcu)
    newsSites.append(haberturk)
    newsSites.append(sondakika)
    newsSites.append(internethaber)
    newsSites.append(ntv)
    newsSites.append(cnn)

    counter = [0, 0]

    def getNews(self, save=0, _delay=1):
        self.delay = _delay
        for siterow in self.newsSites:
            self.drawline(30)
            sitename = siterow.getsitename()
            r = requests.get(siterow.getsiteurl())
            source = BeautifulSoup(r.content, "lxml")
            data = source.select(siterow.getcontenttarget())
            print(siterow.sitename)
            counter = 0
            for x in data:
                counter += 1
                if x["title"] != "":
                    if (x["href"].split("/"))[0] == "":
                        x["href"] = siterow.siteurl[:-1] + x["href"]
                    if save:
                        self.savenews(sitename, (x["title"]).lower().replace("'", "\\'"), x["href"], "")
                        print("|", end="")
                    else:
                        print(x["title"].lower())
            print(counter)
        print("\n " + str(datetime.datetime.now().time()) + "\n News count >> " + str(
            self.newcount()) + "\n New news >> " + str(self.newnewscount()) + "\n Average >>" + str(self.average()))

    def drawline(self, count):
        print('\n')
        for x in range(int(count)):
            print("-", end="")
        print('\n')

    def savenews(self, sitename, title, link, img):
        db = database.database()
        insert = db.insert("all_news",
                           [["news_title", title], ["news_site", sitename], ["news_link", link], ["news_image", img]],
                           [["news_title", title]])

    def getcount(self):
        db = database.database()
        self.counter = self.counter[1], int(db.getnum("all_news")[0])
        return self.counter[1]

    def average(self):
        return self.newnewscount() / self.delay

    def newnewscount(self):
        return self.counter[1] - self.counter[0]

    def newcount(self):
        return self.getcount()
