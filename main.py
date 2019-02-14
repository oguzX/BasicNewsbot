import newsrequest
import time

news = newsrequest.newsrequest()

delay = 480

while 1:
    news.getNews(1,delay)
    time.sleep(delay)
