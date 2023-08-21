import requests
from bs4 import BeautifulSoup as bs
import fake_useragent

import pandas as pd
import json
import itertools


INPUT_FILE = '../rc/hh.ru-hrefs.csv'
OUTPUT_FILE = '/rc/hh.ru-vacancies_data.csv'


def get_vacancies_data(input_file_with_urls: str):
    proxylist_file = open('../rc/proxylist.json', encoding="UTF-8")
    proxy_list = json.load(proxylist_file)['data']
    proxylist_file.close()

    num_of_proxy = itertools.cycle(range(len(proxy_list)))
    ua = fake_useragent.UserAgent()

    #urls_file = open(input_file_with_urls, encoding="UTF-8")
    urls = pd.read_csv(input_file_with_urls, sep=';', )  # DataFrame(data=urls_file)
    #urls_file.close()

    vacancy_list = pd.DataFrame(columns=['name', 'salary', 'description', 'key skills'])
    print(urls.head())
    for index, row in urls.iterrows():
        r = requests.get(row['url'], headers={"user-agent": ua.random}, proxies=proxy_list[next(num_of_proxy)])

        if r.status_code != 200 or r.status_code != 200:
            print(f"\nERROR: cannot create connection to {r.url}\nstatus code {r.status_code}\n")
            return None

        print(f"parsing {index} {r.url}")

        # находим все вакансии на текущей странице
        soup = bs(r.text, "html.parser")  # lxml

        title = soup.find(class_='vacancy-title')
        name = title.find(class_='bloko-header-section-1').text
        salary = title.find(class_='bloko-header-section-2 bloko-header-section-2_lite')
        if salary:
            salary = salary.text

        description = ''
        description_all = soup.find(class_='vacancy-description').find(class_='g-user-content')
        if description_all:
            description = description_all.text
        else:
            description = description_all.find(class_='tmpl_hh_wrapper').text

        key_skills = [item.text for item in \
                      soup.find(class_='bloko-tag-list').find_all(class_='bloko-tag__section')]

        vacancy_list.loc[index] = [name, salary, description, key_skills]

        r.close()

    return vacancy_list


if __name__ == '__main__':
    file = pd.DataFrame(data=get_vacancies_data(INPUT_FILE))
    file.to_csv(OUTPUT_FILE, sep=';', index=False)



