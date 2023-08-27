import requests
import json
import time
from itertools import count


TEXT = 'python'
PATH = 'rc/find_results/'
# SUBPATH = '/vacancies_description/'


def get_ids_in_page(params, vac_count: int):
    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    vacancies = [int(item['id']) for item in json.loads(data)['items']]
    return vacancies, len(vacancies)


def pages(params):
    time.sleep(0.3)
    req = requests.get('https://api.hh.ru/vacancies', params)
    num_of_vacancies = int(json.loads(req.text)['found'])
    max_page = num_of_vacancies // params['per_page']
    if max_page > 2000 // params['per_page']:
        max_page = 2000 // params['per_page']
    req.close()
    return max_page


vacancy_ids = []
page_count = count()
vacancies_count = 0
for area in range(1, 5):  # От Москвы до Новосибирска
    print(area)
    params = {
        'text': TEXT,  # Текст фильтра. В имени должно быть слово "Аналитик"
        'area': area,  # Поиск ощуществляется по вакансиям города Москва
        'page': 0,  # Индекс страницы поиска на HH
        'per_page': 100  # Кол-во вакансий на 1 странице
    }
    max_page = pages(params)
    for page in range(0, max_page + 1):
        next(page_count)
        # Преобразуем текст ответа запроса в справочник Python
        page_ids, num = get_ids_in_page(params, vacancies_count)
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
path_file = PATH + 'text=' + TEXT + '/vacancy_ids.dat'
#os.mkdir(path_dir)
with open(path_file, mode='w') as f:
    f.write('\n'.join(str(id) for id in vacancy_ids))
# делаем редактирование в других файлах.py
print('Страницы поиска собраны, всего страниц:', next(page_count), ', всего вакансий:', vacancies_count)
