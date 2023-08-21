import json
from datetime import datetime


print('который' == 'который̆')
words = dict()
with open('./rc/find_results/text=python_words.json', encoding="UTF-8") as f:
    words = json.load(f)
    for word_normalized in words:
        words[word_normalized] = dict(sorted(words[word_normalized].items(), key=lambda x: x[1], reverse=True))
    words = dict(sorted(words.items(), key=lambda x: x[1]['count'], reverse=True))


print(str(datetime.now())[:-3])
