import json
import os
import time
from datetime import datetime
from itertools import count

import requests
from bs4 import BeautifulSoup as bs

PATH = './rc/find_results/'
URL = 'https://api.hh.ru/vacancies/'
MAX_ERROR_INDEX = 10


with os.scandir(PATH) as files:
    for filename in (file.name for file in files if file.is_file() and file.name[-4:] == '.dat'):
        filepath = PATH + filename[:filename.rindex('.')]
        if not os.path.exists(filepath):
            # создаём отдельную папку для каждого запроса
            os.mkdir(filepath)
        # перебираем файлы-ответы
        with open(PATH + filename) as f:
            error_index = count()
            name_index = count()

            get_vacancies_data_log = open(PATH + filename[:filename.rindex('.')] + '.log', 'a', encoding="UTF-8")
            for indx, id in enumerate(f.readlines()):
                time.sleep(0.5)
                r = requests.get(URL + id[:-1])
                if r.status_code != 200 or r.status_code != 200:
                    print(f"\nERROR: cannot create connection to {r.url}\nstatus code {r.status_code}")
                    get_vacancies_data_log.write(f'{str(datetime.now())[:-3]}: ERROR, URL {r.url}, status code {r.status_code}\n')
                    if next(error_index) > MAX_ERROR_INDEX:
                        print("Вы забанены")
                        break
                    continue

                data = json.loads(r.content.decode())
                soup = bs(data['description'], "html.parser")
                job_info = {
                    'description': soup.get_text().strip(),
                    'key_skills': [skill['name'] for skill in data['key_skills']]
                }

                file_output_name = ''.join([c for c in data['name'] if c not in r'\/:*?"<>|"'])
                if not os.path.exists(filepath + '/' + file_output_name + '.json'):
                    full_file_output_name = filepath + '/' + file_output_name + '.json'
                    with open(full_file_output_name, 'w', encoding="UTF-8") as file_output:
                        file_output.write(json.dumps(job_info, ensure_ascii=False))
                        print(indx, id[:-1])
                else:
                    full_file_output_name = filepath + '/' + file_output_name + str(next(name_index)) + '.json'
                    print(full_file_output_name, 'уже существует!')
                    #get_vacancies_data_log.write(f'rename file, PATH: {full_file_output_name}\n')
                    with open(full_file_output_name, 'w', encoding="UTF-8") as file_output:
                        file_output.write(json.dumps(job_info, ensure_ascii=False))
                        print(indx, id[:-1])
            #print("Уникальных названий", name_index)
            get_vacancies_data_log.close()

