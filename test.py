import copy
import json
from datetime import datetime
import io
import re


print('который' == 'который̆')


def lst_plus_1(lst):
    lst[0] = 0
    lst.append(5)


print(str(datetime.now())[:-3])
text = 'test.tst'
lst = [1, 2, 3, 4]
lst1 = copy.deepcopy(lst)
lst_plus_1(lst)
lst1.append(5)
lst1.append(6)
lst1[0] = 0
lst.append(6)


print(text[:-4], lst, lst1, lst == lst1, lst is lst1)
print(id(lst[1]), id(lst1[1]))



# max len of the line---------------------------------------------------------------------------------------------------

def words_from_vacancies_names():
    path = './rc/find_results/python'
    with open(path + '/uniq_names.json', encoding="UTF-8") as f_words:
        names = json.loads(f_words.read())
        with open(path + '/uniq_names_words.json', 'w', encoding="UTF-8") as f_words_en:
            words_dict = dict()
            for name in names:
                name_lower = re.sub(r'[^a-zA-Zа-яА-Я ]', ' ', name.lower())
                words = name_lower.split()
                for word in words:
                    if word in words_dict:
                        words_dict[word] += names[name]
                    else:
                        words_dict[word] = dict()
                        words_dict[word] = names[name]

            words_dict = dict(sorted(words_dict.items(), key=lambda x: x[1], reverse=True))
            f_words_en.write(json.dumps(words_dict, indent=2, ensure_ascii=False))
def words_from_vacancies_names_with_outer():
    path = './rc/find_results/python'
    with open(path + '/uniq_names.json', encoding="UTF-8") as f_words:
        names = json.loads(f_words.read())
        with open(path + '/uniq_names_words_with_outer.json', 'w', encoding="UTF-8") as f_words_en:
            words_dict = dict()
            for name in names:
                name_lower = re.sub(r'[^a-zA-Zа-яА-Я ]', ' ', name.lower())
                words = name_lower.split()
                for word in words:
                    if word in words_dict:
                        words_dict[word]['count'] += names[name]
                    else:
                        words_dict[word] = dict()
                        words_dict[word]['count'] = names[name]

                    words_outer = [word_outer for word_outer in words if word_outer != word]
                    for word_outer in words_outer:
                        if word_outer in words_dict[word]:
                            words_dict[word][word_outer] += names[name]
                        else:
                            words_dict[word][word_outer] = names[name]
            for word in words_dict:
                words_dict[word] = dict(sorted(words_dict[word].items(), key=lambda x: x[1], reverse=True))
            words_dict = dict(sorted(words_dict.items(), key=lambda x: x[1]['count'], reverse=True))
            f_words_en.write(json.dumps(words_dict, indent=2, ensure_ascii=False))


words_from_vacancies_names_with_outer()
words_from_vacancies_names()