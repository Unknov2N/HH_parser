import json
import random
import time
from datetime import datetime
import itertools

# import fake_useragent
import requests
from bs4 import BeautifulSoup as bs

import os  # в чем разница между os.scandir и pathlib.iterdir?
from pathlib import Path
from shutil import rmtree
from get_vacanciesID_by_API import create_dir

PATH = './rc/find_results/'  # general requests directory
TEXT = 'Архитектор «зеленых» городов'
URL = 'https://api.hh.ru/vacancies/'  # api vacancies address
MAX_ERROR_INDEX = 10  # for 304 status code
CHARS_TO_DELETE_IN_FILENAME = r'\/:*?"<>|"'  # for naming identical files
TIMEOUT = 0.3  # for time.sleep


def dict_count_and_sort_by_value(vacancies: dict):
    vacancies = dict(sorted
                     (sorted(list(vacancies.items()), key=lambda x: x[0]),
                      key=lambda x: x[1]['count'], reverse=True))
    for vacancy in vacancies:

        vacancies[vacancy]['key_skills'] = dict(sorted
                                                (sorted(list(vacancies[vacancy]["key_skills"].items()),
                                                        key=lambda x: x[0]),
                                                 key=lambda x: x[1], reverse=True))
        vacancies[vacancy]["key_skills"]['count'] = len(vacancies[vacancy]["key_skills"])
    vacancies['count'] = len(vacancies)
    return vacancies


# proxylist_file = open('rc/proxylist.json')
# proxy_list = json.load(proxylist_file)['data']
# num_of_proxy = itertools.cycle(range(len(proxy_list)))
# ua = fake_useragent.UserAgent()

def delete_all_files_in_dir(path: str):
    create_dir(path)
    for path in Path(path).iterdir():
        if path.is_dir():
            rmtree(path)
        else:
            path.unlink()


def collect_vacancies_info(path=PATH + TEXT, timeout=TIMEOUT):
    # перебираем файлы-ответы
    with open(path + '/vacancy_ids.dat') as vacancy_ids:
        delete_all_files_in_dir(path + '/vacancies_description')
        time.sleep(random.randint(3, 30))  # задержка между text={}
        error_index = itertools.count()
        uniq_names = dict()
        uniq_key_skills = dict()

        get_vacancies_data_log = open(path + '/logs.log', 'a', encoding="UTF-8")
        for indx, id in enumerate(vacancy_ids.readlines()):
            time.sleep(timeout)
            # check_request = 0
            requests_tries = 0  # for breaking "while" and raise ConnectionError
            while not requests_tries:
                try:
                    r = requests.get(URL + id[:-1])
                    # check_request = False
                    requests_tries = 1
                except requests.exceptions.ConnectTimeout as e:
                    print(e)
                    requests_tries += 1
                    if requests_tries > 1 + MAX_ERROR_INDEX:
                        raise requests.exceptions.ConnectionError
                    time.sleep(13 * 60 + 13 + random.randint(-61, 61))

            # , headers={"user-agent": ua.random} , proxies=proxy_list[next(num_of_proxy)])
            if r.status_code != 200 or r.status_code != 200:
                print(indx, id[:-1], 'ERROR,', r.status_code, r.url)
                get_vacancies_data_log.write(f'{str(datetime.now())[:-3]}: ERROR, URL {r.url}, '
                                             f'status code{r.status_code}\n')
                if r.status_code == 403:
                    if next(error_index) > MAX_ERROR_INDEX:
                        print("Вы забанены")
                        break
                continue
            error_index = itertools.count()
            data = json.loads(r.content.decode())
            soup = bs(data['description'], "html.parser")
            job_info = {
                'description': soup.get_text().strip(),
                'key_skills': [skill['name'] for skill in data['key_skills']],
                'salary': data['salary']
            }


            vacancy_name = data['name']
            for key_skill in job_info['key_skills']:
                if key_skill in uniq_key_skills:
                    uniq_key_skills[key_skill] += 1
                else:
                    uniq_key_skills[key_skill] = 1

            vacancy_name_to_file = ''.join([c for c in data['name'] if c not in CHARS_TO_DELETE_IN_FILENAME])
            if not vacancy_name in uniq_names:  # os.path.exists(filepath + '/' + file_output_name + '.json'):
                uniq_names[vacancy_name] = dict()
                uniq_names[vacancy_name]['count'] = 1
                uniq_names[vacancy_name]['key_skills'] = dict()
                for skill in job_info['key_skills']:
                    uniq_names[vacancy_name]['key_skills'][skill] = 1
                # тут должно быть приравнивание ключевых навыков (осторожно в блоке else, нужно грамотно задеть существующие и добавить новые)

                full_file_output_name = path + '/vacancies_description/' + vacancy_name_to_file + '.json'
                print(indx, id[:-1], vacancy_name)
            else:
                full_file_output_name = path + '/vacancies_description/' + vacancy_name_to_file + ' (' \
                                        + str(uniq_names[vacancy_name]['count']) + ').json'
                #get_vacancies_data_log.write(f'rename file, PATH: {full_file_output_name}\n')
                print(f'{indx} {id[:-1]} '
                      f'{vacancy_name} ({uniq_names[vacancy_name]["count"]})')
                uniq_names[vacancy_name]['count'] += 1
                for skill in job_info['key_skills']:
                    if skill in uniq_names[vacancy_name]['key_skills']:
                        uniq_names[vacancy_name]['key_skills'][skill] += 1
                    else:
                        uniq_names[vacancy_name]['key_skills'][skill] = 1

            with open(full_file_output_name, 'w', encoding="UTF-8") as file_output, \
                    open(full_file_output_name[:-5] + '_full.json', 'w', encoding="UTF-8") as file_full_job_info:
                file_output.write(json.dumps(job_info, ensure_ascii=False))
                file_full_job_info.write(json.dumps(data, ensure_ascii=False))

        uniq_names_withount_keys = {key: uniq_names[key]['count'] for key in uniq_names}
        uniq_names_withount_keys = dict(sorted(list(uniq_names_withount_keys.items()),
                                               key=lambda x: x[1], reverse=True))

        uniq_names = dict_count_and_sort_by_value(uniq_names)
        # рассортировать по алфавиту одинаковые по количеству названия -- проверить
# добавить в название ключевые навыки и их количество. сортируем сначала по количеству, потом по алфавиту (де-факто наоборот) (сделать функцию добавления количества и сортировки)
        print("Уникальных названий:", uniq_names['count'])
        with open(path + '/uniq_names_with_keys.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(uniq_names, indent=2, ensure_ascii=False))
        with open(path + '/uniq_names.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(uniq_names_withount_keys, indent=2, ensure_ascii=False))

        uniq_key_skills = dict(sorted(list(uniq_key_skills.items()), key=lambda x: x[1], reverse=True))
        uniq_key_skills['count'] = len(uniq_key_skills)
        with open(path + '/uniq_key_skills.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(uniq_key_skills, indent=2, ensure_ascii=False))

        get_vacancies_data_log.close()

# proxylist_file.close()

if __name__ == '__main__':
    collect_vacancies_info()