import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import itertools

FILE_NAME = "rc/hh.ru-hrefs" + ".csv"
URL_SITE = "https://novosibirsk.hh.ru/search/vacancy?text=&salary=&ored_clusters=true&area=4&page="  # page обязательно в конце
'''
text -- текст запроса
salary -- минимальная зарплата
ored_clusters -- хз
area -- регион; 1 - Москва, 2 Питер, 3 Ебург, 4 Нск
page -- номер отображаемой страницы конечного поиска
'''


def get_hrefs(request: str):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'} # без этого r.status_code == 404 почему-то
    
    vacancy_list = {'title': [], 'url': []}
    with open('rc/proxylist.json') as proxylist_file:
        
        proxy_list = json.load(proxylist_file)['data']
        num_of_proxy = itertools.cycle(range(len(proxy_list)))
       
        for numpage in itertools.count():
            
            place_to_insert_request = URL_SITE.index('?text=') + 6
            place_to_insert_numpage = URL_SITE.index('&page=') + 6
            url = URL_SITE[:place_to_insert_request] + request + URL_SITE[place_to_insert_request:] + str(numpage)
            
            r = requests.get(url, headers=headers, proxies=proxy_list[next(num_of_proxy)])
            if not r.status_code == 200:
                print(f"\nERROR: cannot create connection to {r.url}\nstatus code {r.status_code}\n")
                return None
            else:
                print(f"parsing {r.url}\npage {numpage}")

            # находим все вакансии на текущей странице
            soup = bs(r.text, "html.parser")  # lxml
            vacancy_elements = soup.find_all(class_='serp-item__title')
            if vacancy_elements == []:
                print(f"Last valuable page is {numpage - 1}\n")
                break
            
            print(len(vacancy_elements))
            for each_part in vacancy_elements:
                vacancy_list['title'].append(each_part.text)
                vacancy_list['url'].append(each_part.get('href'))

    return vacancy_list


if __name__ == '__main__':
    
    # rq = input().replace("+", ' ')
    rq = 'python'

    file = pd.DataFrame(data=get_hrefs(rq))
    file.to_csv(FILE_NAME, sep=';', index=False)


    