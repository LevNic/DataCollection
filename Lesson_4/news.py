from pprint import pprint
from lxml import html
from datetime import datetime

import requests
import re


def yandex_news():
    try:
        response = requests.get('https://yandex.ru')
        root = html.fromstring(response.text)
        yandex = root.xpath('//ol/li/a/@aria-label|//ol/li/a/@href|//ol/li/a/span/div/object/@title')

        news = []
        all_news = [news]
        date = datetime.now().date().strftime("%d.%m.%Y")

        for n in range(0, len(yandex), 3):
            for i in range(n, n + 3):
                news.append(yandex[i])
            news.append(date)
            all_news.append(news)
            news = []
        return all_news
    except:
        print('Somesing went wrong')

# С майла-ру мне так и не удалось получить данные.
def mail_news():
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    try:
        response = requests.get('https://mail.ru', headers = header)
        root = html.fromstring(response.text)
        result = root.xpath('//ul')
        return result
    except:
        print('Somesing went wrong')

def lenta_news():
    
    try:
        response = requests.get('https://lenta.ru/')
        root = html.fromstring(response.text)
        lenta = root.xpath("//div[@class='span4'][2]/div[@class='item']/a/text()| \
                            //div[@class='span4'][2]/div[@class='item']/a/time/@title| \
                            //div[@class='span4'][2]/div[@class='item']/a/@href")

    except:
        print('Somesing went wrong')
    
    news = []
    all_news = [news]

    for n in range(0, len(lenta), 3):
        for i in range(n, n + 3):
            news.append(lenta[i])
        news[-1] = re.sub('\xa0', ' ',  news[-1]) 
        news.insert(2, 'Lenta.ru')
        all_news.append(news)
        news = []

    return all_news

yandex = yandex_news()
pprint(yandex)
print('*' * 52)

lenta = lenta_news()
pprint(lenta)

