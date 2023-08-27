### HH_parser

1. __get_proxy_list__ выгружает из _proxylist.geonode.com_ в __/rc/proxylist.txt__ актуальные прокси (~5000 шт)
2. **get_vacanciesID_by_API.py** получает все ID вакансий в __/rc/find_results/text={TEXT}.dat__ (не более 2000) — внутри в переменной TEXT указать поисковый запрос 
> альтернативное развитие (отброшено; скрипты находятся в __/ost/__):  
> - requests - из страницы парсится 20 из 50 вакансий (виноват JS)
> - selenium - рабочий способ, но страница долго загружается



3. **get_vacancies_data_from_IDs.py** загружает инфо о каждой вакансии (только description и key_skills) по ID из
  __/rc/find_results/text={TEXT}.dat__ в папку __/rc/find_results/text={TEXT}/__; в __/rc/find_results/text={TEXT}.log__ пишутся ошибки соединения;
    для выгрузки вакансии используЮтся прокси из файла _proxylist.json_  
4. __words_list.py__ формируется список наиболее употребляемых слов в разных формах, со списком следующих за ними слов 
    (аналог подсказок сверху клавиатуры смартфона при наборе текста) в файл **/rc/find_results/text={TEXT}_words.json**; 
    в **/rc/find_results/text={TEXT}_key_skills.json** пишутся все попавшиеся ключевые навыки;
    к каждому слову в обоих файлах прикреплено количество употребления и произведена сортировка слов по этому значению  

##### text={TEXT}_words.json
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

