from functools import reduce
from itertools import count
import os
import json
import pymorphy3
from datetime import datetime

PATH = './rc/find_results/text=python'
CHARS_TO_DELETE = r"~[]{};,.|!@#$%^&*()_+`\"'№;:?="


# read results of all search requests
def collect_words_from_vacancies_info(path=PATH):
    words = dict()
    #key_skills = dict()
    morph = pymorphy3.MorphAnalyzer()
    vacancies_path = path + '/vacancies_description'
    file_num = count()
    log = open(path + '/logs.log', 'a', encoding="UTF-8")
    time1 = datetime.now()
    log.write (f'{datetime.now():} words_list; START scanning vacancies\n')
    count_vacancies = count()
    with os.scandir(vacancies_path) as vacancies:
        # processing data of each vacancy

        for vacancy in vacancies:
            next(count_vacancies)
            print('processing', next(file_num))
            with open(vacancies_path + '/' + vacancy.name, encoding="UTF-8") as vac_file:
                js_vac_file = json.loads(vac_file.read())
                text = js_vac_file['description']
                text_formatted = ''.join(c for c in text if c not in CHARS_TO_DELETE).lower()
                # create key skills list
                '''for skill in js_vac_file['key_skills']:
                    if skill in key_skills:
                        key_skills[skill] += 1
                    else:
                        key_skills[skill] = 1'''
                # creating words list
                 #СОЗДАТЬ ФУНКЦИЮ processing_text(text_words)
                 #с внутренней функцией processing_word(words, index, word)
                text_words = text_formatted.split()
                for index, word in enumerate(text_words):
                    word_next = None
                    if index < len(text_words) - 1:
                        word_next = text_words[index + 1]

                    #processing_word(words, index, word)
                    word_normalized = morph.parse(word)[0].normal_form
                    if word_normalized in words:
                        if word in words[word_normalized]:
                            words[word_normalized][word]['count'] += 1
                            if word_next:
                                if word_next in words[word_normalized][word]:
                                    words[word_normalized][word][word_next] += 1
                                else:
                                    words[word_normalized][word][word_next] = 1
                        else:
                            words[word_normalized][word] = dict()
                            words[word_normalized][word]['count'] = 1
                            if word_next:
                                words[word_normalized][word][word_next] = 1

                    else:
                        words[word_normalized] = dict()
                        words[word_normalized][word] = dict()
                        words[word_normalized][word]['count'] = 1
                        if word_next:
                            words[word_normalized][word][word_next] = 1

    # sorting data by frequency
    for word_normalized in words:
        for word in words[word_normalized]:
            # sorting next words by them frequency
            words[word_normalized][word] = dict(sorted(
                dict(sorted(words[word_normalized][word].items(), key=lambda x: x[0])).items(),
                key=lambda x: x[1], reverse=True))
        # sorting words in normalized word dict
        words[word_normalized] = dict(sorted(
            dict(sorted(words[word_normalized].items(), key=lambda x: x[0])).items(),
            key=lambda x: x[1]['count'], reverse=True))
        # count normalize words by counting all daughter words
        words[word_normalized]['count'] = \
            reduce(lambda x, y: x + y, [words[word_normalized][word]['count'] for word in words[word_normalized]])
    # sorting normalized words
    words = dict(sorted(words.items(), key=lambda x: x[1]['count'], reverse=True))
    # key_skills = dict(sorted(key_skills.items(), key=lambda x: x[1], reverse=True))
    # saving all data
    with open(path + '/words_with_next.json', 'w', encoding="UTF-8") as f_words:
        f_words.write(json.dumps(words, indent=2, ensure_ascii=False))
    with open(path + '/words.json', 'w', encoding="UTF-8") as f_words:
        words_without_next = dict(sorted({i: words[i]['count'] for i in list(words.keys())}.items(),
                                         key=lambda x: x[1], reverse=True))
        f_words.write(json.dumps(words_without_next, indent=2, ensure_ascii=False))
    '''with open(PATH + '/' + filename + '/key_skills.json', 'w', encoding="UTF-8") as f_key_skills:
        f_key_skills.write(json.dumps(key_skills, indent=2, ensure_ascii=False))'''
    time2 = datetime.now()
    delta_time = (time2 - time1).total_seconds()
    num_of_vacancies = next(count_vacancies)
    log.write(f'{datetime.now():} words_list; {num_of_vacancies} vacancies scanned, '
              f'{delta_time} seconds passed, '
              f'{num_of_vacancies / delta_time } per sec processed; STOP\n')
    log.close()

if __name__ == '__main__':
    collect_words_from_vacancies_info()