from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import fake_useragent

import pandas as pd
import json
import time
import random

import itertools
import copy

FILE_NAME = "rc/hh.ru-hrefs_python_Moscow" + ".csv"
URL_SITE = "https://novosibirsk.hh.ru/search/vacancy"  # ?text=&salary=&ored_clusters=true&area=4&page="
URL_SITE_ = "https://novosibirsk.hh.ru/search/vacancy"  # ?text=&salary=&ored_clusters=true&area=4&page="
'''
text -- текст запроса
salary -- минимальная зарплата
area -- регион; 1 - Москва, 2 Питер, 3 Ебург, 4 Нск
page -- номер отображаемой страницы конечного поиска
'''
KEYS = {'area': 1, 'page': None, 'text': None, 'salary': None}
REQUEST = 'python'


def get_hrefs_selenium(query: str, area: int):
    vacancy_list = {'title': [], 'url': []}

    keys = copy.deepcopy(KEYS)
    keys['text'] = query

    ua = fake_useragent.UserAgent()
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.headless = True
    chrome_options.add_argument('--user-agent=' + ua.random)
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--proxy-server=%s' % f"{proxy['ip']}:{proxy['port']}")
    browser = webdriver.Chrome(options=chrome_options)

    with open('../rc/proxylist.json') as proxylist_file:

        proxy_list = json.load(proxylist_file)['data']
        num_of_proxy = itertools.cycle(range(len(proxy_list)))

        for numpage in itertools.count():
            proxy = proxy_list[next(num_of_proxy)]
            keys['page'] = numpage
            url = f"https://novosibirsk.hh.ru/search/vacancy?text={query}&area={area}&page={numpage}"
            browser.get(url)
            time.sleep(random.rand() + 0.14)

            # тут должна быть проверка на status code == 200

            print(f"parsing {browser.current_url}\npage {numpage} —", end=' ')

            # находим все вакансии на текущей странице
            #vacancy_elements = browser.find_elements(By.CLASS_NAME, "serp-item__title")
            soup = bs(browser.page_source, "html.parser")  # lxml
            vacancy_elements = soup.find_all(class_='serp-item__title')
            if not vacancy_elements:
                print(f"Last valuable page is {numpage - 1}\n")
                break

            print(len(vacancy_elements), 'vacancies\n')
            for each_part in vacancy_elements:
                vacancy_list['title'].append(each_part.text)
                vacancy_list['url'].append(each_part.get('href'))

    browser.close()
    return vacancy_list


if __name__ == '__main__':
    file = pd.DataFrame(data=get_hrefs_selenium(REQUEST, 1))
    file.to_csv(FILE_NAME, sep=';', index=False)
