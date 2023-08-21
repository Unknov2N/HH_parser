from functools import reduce
from itertools import count
import os
import json
import pymorphy3

PATH = './rc/find_results/'
CHARS_TO_DELETE = r"~[]{};,.|!@#$%^&*()_+`\"'№;:?="

# read results of all search requests
with os.scandir(PATH) as find_results:
    for filename in (file.name for file in find_results if file.is_dir()):
        words = dict()
        key_skills = dict()
        morph = pymorphy3.MorphAnalyzer()
        vacancies_path = PATH + filename
        file_num = count()
        with os.scandir(vacancies_path) as vacancies:
            # processing data of each vacancy
            for vacancy in vacancies:
                print('processing', next(file_num))
                with open(vacancies_path + '/' + vacancy.name, encoding="UTF-8") as vac_file:
                    js_vac_file = json.loads(vac_file.read())
                    text = js_vac_file['description']
                    text_formatted = ''.join(c for c in text if c not in CHARS_TO_DELETE).lower()
                    # create key skills list
                    for skill in js_vac_file['key_skills']:
                        if skill in key_skills:
                            key_skills[skill] += 1
                        else:
                            key_skills[skill] = 1
                    # create words list
                    text_words = text_formatted.split()
                    for index, word in enumerate(text_words):
                        word_next = None
                        if index < len(text_words) - 1:
                            word_next = text_words[index + 1]
                        word_normalized = morph.parse(word)[0].normal_form
                        if word_normalized in words:
                            if word in words[word_normalized]:
                                words[word_normalized][word]['count'] += 1
                                if word_next in words[word_normalized][word] and word_next:
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
                '''
                {word_norm_1: 
                    {word1: 
                        {
                        next1_word1: M
                        next2_word1: N
                        count_word1: O
                        ...
                        },
                    word2:
                        {
                        next1_word2: A
                        next2_word2: B
                        count_word2: C
                        },
                    count_word_norm_1: Z
                    },
                word_norm_2:
                    ...
                '''

        # sorting data by frequency
        for word_normalized in words:
            for word in words[word_normalized]:
                # sorting next words by them frequency
                words[word_normalized][word] = dict(sorted(words[word_normalized][word].items(),
                                                           key=lambda x: x[1], reverse=True))
            # sorting words in normalized word dict
            words[word_normalized] = dict(sorted(list(words[word_normalized].items()),
                                                 key=lambda x: x[1]['count'], reverse=True))
            # count normalize words by counting all daughter words
            words[word_normalized]['count'] = \
                reduce(lambda x, y: x + y, [words[word_normalized][word]['count'] for word in words[word_normalized]])
        # sorting normalized words
        words = dict(sorted(words.items(), key=lambda x: x[1]['count'], reverse=True))
        key_skills = dict(sorted(key_skills.items(), key=lambda x: x[1], reverse=True))
        # saving all data
        with open(PATH + '/' + filename + '_words.json', 'w', encoding="UTF-8") as f_words:
            f_words.write(json.dumps(words, indent=2, ensure_ascii=False))
        with open(PATH + '/' + filename + '_key_skills.json', 'w', encoding="UTF-8") as f_key_skills:
            f_key_skills.write(json.dumps(key_skills, indent=2, ensure_ascii=False))
