import requests
import json


URL_SITE = "https://novosibirsk.hh.ru/search/vacancy?text=&salary=&area=4&ored_clusters=true"
place_to_insert = URL_SITE.index('?text=') + 6
# r = requests.get(URL_SITE[:place_to_insert] + input().replace("+", ' ') + URL_SITE[place_to_insert:])
print(URL_SITE[:place_to_insert] + input().replace(" ", '+') + URL_SITE[place_to_insert:])