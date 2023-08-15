### HH_parser

1. __get_proxy_list__ выгружает из _proxylist.geonode.com_ в _rc/proxylist.txt_ актуальные прокси (~5000 шт)
1. **get_hrefs.py** получает все ссылки на вакансии в ___hh.ru-hrefs.csv___ (сделано, но надо учесть подгрузку через js https://ru.stackoverflow.com/questions/1229289/requests-%d0%bd%d0%b5-%d0%bf%d0%be%d0%b4%d0%b3%d1%80%d1%83%d0%b6%d0%b0%d0%b5%d1%82-%d1%81%d1%82%d1%80%d0%b0%d0%bd%d0%b8%d1%86%d1%83-%d1%86%d0%b5%d0%bb%d0%b8%d0%ba%d0%be%d0%bc-python)

2. **parsing_hrefs.py** парсит инфу о  ПИФах по ссылкам из ___investfunds.ru-hrefs.csv___ в *__investfunds-PIFs.csv__*; подгружает прокси из файла _proxylist.txt_

3. **analytics.py** делает ковариационную матрицу из данных *__investfunds-PIFs.csv__*, визуализирует в картинку ___heatmap.png___

~~- **test.py** хранит временный код (черновик)~~