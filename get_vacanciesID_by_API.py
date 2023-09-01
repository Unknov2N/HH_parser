import requests
import json
import time
from itertools import count
import os
import fake_useragent
import random


TIMEOUT = 0.3
TEXT = 'программист 1C'
PATH = './rc/find_results/'
# SUBPATH = '/vacancies_description/'


def get_ids_in_page(params, useragent, timeout=TIMEOUT):
    time.sleep(timeout)
    is_connected = False
    while is_connected is False:
        try:
            req = requests.get('https://api.hh.ru/vacancies', params, headers={"user-agent": useragent})  # Посылаем запрос к API
            data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
            req.close()
            vacancies = [int(item['id']) for item in json.loads(data)['items']]
            is_connected = True
        except KeyError as e:
            print(e, '; timeout 13 minutes')
            time.sleep(13 * 60 + 13 + random.randint(-61, 61))

    return vacancies, len(vacancies)


def num_of_pages(params, useragent, timeout=TIMEOUT):
    time.sleep(7 + random.randint(-5, 5))
    req = requests.get('https://api.hh.ru/vacancies', params, headers={"user-agent": useragent})
    num_of_vacancies = int(json.loads(req.text)['found'])
    max_page = num_of_vacancies // params['per_page']
    if max_page > 2000 // params['per_page']:
        max_page = 2000 // params['per_page']
    req.close()
    return max_page


def collect_vacancies_id(text=TEXT, path=PATH, timeout=TIMEOUT):
    ua = fake_useragent.UserAgent()
    vacancy_ids = []
    page_count = count()
    vacancies_count = 0
    for area in range(1, 5):  # От Москвы до Новосибирска
        print(f'request is {text}, area is {area}')
        params = {
            'text': text,  # Текст фильтра. В имени должно быть слово "Аналитик"
            'area': area,  # Поиск ощуществляется по вакансиям города Москва
            'page': 0,  # Индекс страницы поиска на HH
            'per_page': 100  # Кол-во вакансий на 1 странице
        }
        max_page = num_of_pages(params, ua.random, timeout=timeout)
        time.sleep(1 + 2 * random.random())
        for page in range(0, max_page + 1):
            next(page_count)
            # Преобразуем текст ответа запроса в справочник Python
            page_ids, num = get_ids_in_page(params, ua.random, timeout=timeout)
            vacancies_count += num
            if page_ids:
                vacancy_ids.extend(page_ids)
            else:
                break

            # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
            print(page + 1, 'of', max_page + 1, 'is processed, vacancies num is:', num)

        # Сохраняем файлы в папку {путь до текущего документа со скриптом}\docs\pagination
        # Определяем количество файлов в папке для сохранения документа с ответом запроса
        # Полученное значение используем для формирования имени документа

        # Создаем новый документ, записываем в него ответ запроса, после закрываем
    create_dir(path)
    path_file = path + '/vacancy_ids.dat'
    with open(path_file, mode='w') as f:
        f.write('\n'.join(str(id) for id in vacancy_ids))
    # делаем редактирование в других файлах.py
    print('Страницы поиска собраны, всего страниц:', next(page_count), ', всего вакансий:', vacancies_count)


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


if __name__ == '__main__':
    collect_vacancies_id()
