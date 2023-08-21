import requests
import json
import time


TEXT = 'python'


def get_ids_in_page(params):
    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return [int(item['id']) for item in json.loads(data)['items']]


def pages():
    req = requests.get('https://api.hh.ru/vacancies', params)
    num_of_vacancies = int(json.loads(req.text)['found'])
    max_page = num_of_vacancies // params['per_page']
    if max_page > 2000 // params['per_page']:
        max_page = 2000 // params['per_page']
    req.close()
    return max_page


vacancy_ids = []
for area in range(1, 5):
    print(area)
    params = {
        'text': TEXT,  # Текст фильтра. В имени должно быть слово "Аналитик"
        'area': area,  # Поиск ощуществляется по вакансиям города Москва
        'page': 0,  # Индекс страницы поиска на HH
        'per_page': 100  # Кол-во вакансий на 1 странице
    }
    max_page = pages()
    for page in range(0, max_page):

        # Преобразуем текст ответа запроса в справочник Python
        page_ids = get_ids_in_page(params)
        if page_ids:
            vacancy_ids.extend(page_ids)
        else:
            break

        # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
        print(page + 1, 'of', max_page, 'is processed')
        time.sleep(1.25)

    # Сохраняем файлы в папку {путь до текущего документа со скриптом}\docs\pagination
    # Определяем количество файлов в папке для сохранения документа с ответом запроса
    # Полученное значение используем для формирования имени документа

    # Создаем новый документ, записываем в него ответ запроса, после закрываем
path_file = './rc/find_results/' + 'text=' + TEXT + '.dat'
#os.mkdir(path_dir)
with open(path_file, mode='w') as f:
    f.write('\n'.join(str(id) for id in vacancy_ids))

print('Страницы поиска собраны')