import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import fake_useragent

import pandas as pd
import json
import time


import itertools
import copy

FILE_NAME = "rc/hh.ru-hrefs" + ".csv"
URL_SITE = "https://novosibirsk.hh.ru/search/vacancy"  # ?text=&salary=&ored_clusters=true&area=4&page="
'''
text -- текст запроса
salary -- минимальная зарплата
area -- регион; 1 - Москва, 2 Питер, 3 Ебург, 4 Нск
page -- номер отображаемой страницы конечного поиска
'''
# HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'} # без этого r.status_code == 404 почему-то
KEYS = {'area': 4, 'page': None, 'text': None, 'salary': None}
REQUEST = 'python'


def get_hrefs_requests_plus_bs(query: str):

    vacancy_list = {'title': [], 'url': []}

    keys = copy.deepcopy(KEYS)
    keys['text'] = query
    ua = fake_useragent.UserAgent()
    session = requests.Session()
    session.headers['User-Agent'] = ua.random

    with open('../rc/proxylist.json') as proxylist_file:
        
        proxy_list = json.load(proxylist_file)['data']
        num_of_proxy = itertools.cycle(range(len(proxy_list)))

        for numpage in itertools.count():

            keys['page'] = numpage
            r = requests.get(URL_SITE, params=keys, headers={"user-agent":ua.random}, proxies=proxy_list[next(num_of_proxy)])
            time.sleep(30)
            if r.status_code != 200 or r.status_code != 200:
                print(f"\nERROR: cannot create connection to {r.url}\nstatus code {r.status_code}\n")
                return None

            print(f"parsing {r.url}\npage {numpage}")

            # находим все вакансии на текущей странице
            soup = bs(r.text, "html.parser")  # lxml
            vacancy_elements = soup.find_all(class_='serp-item__title')
            if not vacancy_elements:
                print(f"Last valuable page is {numpage - 1}\n")
                break
            
            print(len(vacancy_elements))
            for each_part in vacancy_elements:
                vacancy_list['title'].append(each_part.text)
                vacancy_list['url'].append(each_part.get('href'))

            # r.close()
            r.close()

    return vacancy_list


if __name__ == '__main__':
    
    file = pd.DataFrame(data=get_hrefs_requests_plus_bs(REQUEST))
    file.to_csv(FILE_NAME, sep=';', index=False)
