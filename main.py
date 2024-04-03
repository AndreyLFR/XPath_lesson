import requests
from lxml import html
from fake_useragent import UserAgent
import csv
import time

ua = UserAgent()
header = {'User-Agent': ua.chrome}

session = requests.session()
header = {'User-Agent': 'Mozilla/5.0 (<system-information>) <platform> (<platform-details>) <extensions>'}
url = 'https://news.mail.ru/'

response = session.get(url=url, headers=header)
dom = html.fromstring(response.text)

#собираю главные новости news.mail.ru
items_gen_news = dom.xpath("//div[@data-logger='news__MainTopNews']")[0]
links = list(set(items_gen_news.xpath(".//@href")))

#пробегаюсь по ссылкам и собираю данные
news_list = []
for url_news in links:
    dict_ = {}
    response = session.get(url=url_news, headers=header)
    dom = html.fromstring(response.text)
    try:
        dict_['title'] = dom.xpath("//h1[@data-qa='Title']/text()")[0]
        dict_['short_story'] = dom.xpath("//header//p/text()")[0]
    except:
        print(f'c этой новостью что-то не так {url_news}')

    if dict_.get('title', False) and  dict_.get('short_story', False):
        news_list.append(dict_)
    time.sleep(5)

#обработка ошибок не потребовалась
#теперь сохраним
with open('news.csv', 'w', newline='') as csvfile:
    fieldnames = ['title', 'short_story']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for dict_ in news_list:
        writer.writerow(dict_)