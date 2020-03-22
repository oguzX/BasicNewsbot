import newsrequest,database
import time

news = newsrequest.newsrequest()
db = database.database()
delay = 480

while 1:
    news.getNews(1,delay)
    time.sleep(delay)
