from datetime import datetime
import pymorphy3
import json
import random


COUNT_NEXT_WORDS = 5
PATH = 'rc/find_results/'
REQUEST_TEXT = 'python/'


def first_word(word_: str, pymorph: pymorphy3.analyzer.MorphAnalyzer, words: dict):
    while word_:
        word_normalized = pymorph.parse(word_)[0].normal_form
        if not word_normalized in words:
            word_ = input('Такого слова нет в списке. Введите другое слово: ')
        else:
            break
    return word_


def next_word(text_result_, num_next_word_, count_next_words_, morph_, words_, word_):
    if not num_next_word_ > count_next_words_:
        word_normalized = morph_.parse(word_)[0].normal_form
        words_next = tuple(words_[word_normalized][word_].items())
        if count_next_words_ > len(words_next):
            count_next_words_ = len(words_next) - 1
        words_slice = [words_next[word_slice] for word_slice in range(1, count_next_words_ + 1)]
        for index, word in enumerate(words_slice):
            print(f'{index + 1}—{word}', end='  |  ')
        print()
        # print(' | '.join([str(word) for word in words_slice]))

    num_next_word_ = input('Введите номер выбранного слова; '
                          'если хотите закончить, введите 0: ')
    try:
        num_next_word_ = int(num_next_word_)
        if num_next_word_ == 0:
            raise OSError #break
        if num_next_word_ < 0 or num_next_word_ > count_next_words_:
            print('Вы ввели недопустимое число')
            raise TypeError#continue
        word_chosen = words_next[num_next_word_][0]
    except KeyError:
        print('Такого номера нет в списке.')
    except ValueError:
        print('Вы ввели не номер.')
        raise ValueError
        #num_next_word = count_next_words_ + 1
    word_ = word_chosen
    text_result_ += ' ' + word_
    return text_result_, num_next_word_, count_next_words_, morph_, words_, word_


def main():
    count_next_words = COUNT_NEXT_WORDS  # input('Введите необходимое количество следующих слов: ')
    words = dict()
    with open(PATH + REQUEST_TEXT + 'words.json', encoding="UTF-8") as file_words:
        words = json.loads(file_words.read())
    morph = pymorphy3.MorphAnalyzer()

    word = first_word(input('Введите первое слово: '), morph, words)
    text_result = word
    num_next_word = 1

    while num_next_word > 0:
        try:
            text_result, num_next_word, count_next_words, morph, words, word = \
  next_word(text_result, num_next_word, count_next_words, morph, words, word)
            print('TEXT:', text_result)
        except TypeError:
            continue
        except ValueError:
            continue
        except OSError:
            break

    # text_result = text_result[:-1]
    with open(PATH + REQUEST_TEXT + 'text_result.txt', 'a', encoding='u8') as file_text_result:
        file_text_result.write(f'{datetime.now().date()}: {text_result}\n')

    print(f'\nИтоговый текст помещён в {PATH + REQUEST_TEXT + "text_result.txt"}.\n'
          f'Спасибо за использование программы.')


def next_word_robot(text_result_, num_next_word_, morph_, words_, word_, count_next_words_):
    word_normalized = morph_.parse(word_)[0].normal_form
    words_next = tuple(words_[word_normalized][word_].items())
    if count_next_words_ > len(words_next):
        count_next_words_ = len(words_next) - 1
    words_slice = [words_next[word_slice] for word_slice in range(1, count_next_words_ + 1)]
    # print(' | '.join([str(word) for word in words_slice]))
    if num_next_word_ > count_next_words_ - 1:
        raise ValueError
    word_chosen = words_next[num_next_word_][0]
    word_ = word_chosen
    text_result_ += ' ' + word_
    return word_, count_next_words_


def randomized_texts(texts_count_=3, max_words_count_=20, count_next_words_=5):
    file_text_result = open(PATH + REQUEST_TEXT + 'random_text_result.txt', 'a', encoding='u8')
    file_text_result.write(f'texts count: {texts_count_}, words in text count {max_words_count_}, num of possible next words {count_next_words_}\n')
    words = dict()
    with open(PATH + REQUEST_TEXT + 'words.json', encoding="UTF-8") as file_words:
        words = json.loads(file_words.read())
    morph = pymorphy3.MorphAnalyzer()

    for _ in range(texts_count_):
        count_next_words = count_next_words_  # input('Введите необходимое количество следующих слов: ')
        num = random.randint(0, len(words) - 1)
        word = first_word(list(list(words.values())[num])[0], morph, words)
        text_result = word
        # num_next_word = 1

        for _ in range(max_words_count_):#while num_next_word > 0:
            try:
                word, count_next_words = next_word_robot(text_result, random.randint(1, count_next_words), morph, words, word, count_next_words)
            except ValueError:

                continue
            text_result += ' ' + word
        #    text_result, num_next_word, count_next_words, morph, words, word = \
        #next_word_robot(text_result, num_next_word, count_next_words, morph, words, word)
        # print('TEXT:', text_result)

        print(text_result)
        file_text_result.write(f'{datetime.now().date()}: {text_result}\n')
    file_text_result.write('\n')
    file_text_result.close()


if __name__ == '__main__':
    main()
    #randomized_texts()
