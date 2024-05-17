### HH_parser
- __scripts_collector_to_stats__ принимает запросы из __/rc/requests.txt__ и объединяет запуск нижеописанных 
  - __get_vacanciesID_by_API.py__
  - __get_vacancies_data_from_IDs.py__
  - __words_list.py__  
  _в результаты:_  
  - __vacancy_ids.dat__ — ID вакансий для дальнейшего парсинга API hh
  - __vacancies_descriptions/{name}.json__ — полученные в результате парсинга данные о вакансиях после
  - __uniq_names.json__ — уникальные названия вакансий с количеством повторений
  - __uniq_key_skills.json__ — аналогично для ключевых навыков
  - __words.json__ — словарь слов из вакансий с следующими за них словами, с частотой повторения  
1. __get_proxy_list__ выгружает из _proxylist.geonode.com_ в __/rc/proxylist.txt__ актуальные прокси (~5000 шт)
2. **get_vacanciesID_by_API.py** получает все ID вакансий в __/rc/find_results/TEXT/vacancy_ids.dat__ (не более 2000) — внутри в переменной TEXT указать поисковый запрос 
> альтернативное развитие (отброшено; скрипты находятся в __/ost/__):  
> - requests - из страницы парсится 20 из 50 вакансий (виноват JS)
> - selenium - рабочий способ, но страница долго загружается



3. **get_vacancies_data_from_IDs.py** загружает инфо о каждой вакансии (только description и key_skills) по ID из
  __/rc/find_results/TEXT}/vacanciy_ids.dat__ в папку __/rc/find_results/TEXT/vacancies_descriptions__;   
   в **/rc/find_results/TEXT/uniq_names.json** пишутся все уникальные названия вакансий и их повторяемость;  
   в **/rc/find_results/TEXT/uniq_key_skills.json** пишутся все попавшиеся ключевые навыки и их повторяемость;
   в __/rc/find_results/TEXT/logs.log__ пишутся ошибки соединения;  
    ~~для выгрузки вакансии используются прокси из файла _proxylist.json_~~  
4. __words_list.py__ формируется список наиболее употребляемых слов в разных формах, со списком следующих за ними слов 
    (аналог подсказок сверху клавиатуры смартфона при наборе текста) в файл **/rc/find_results/TEXT/words.json**; 
    к каждому слову прикреплено количество употребления и произведена сортировка слов по этому значению  
5. Попытка в интерактивное создание "текста вакансии" из словаря __words.json__;  
   попытка в рандомизированное заполнение (надо переписать)
##### words.json
```json
{
  "word_norm_1": {
    "word1": {
      "next1_word1": A,
      "next2_word1": B,
      ...
      "count_word1": C
    },
    "word2": {
      "next1_word2": M,
      "next2_word2": N,
      ...
      "count_word2": O
    },
    "count_word_norm_1": Z
  },
  "word_norm_2": { 
    ...  
  },
  ...
}

```

- **test.py** хранит временный код (черновик)

