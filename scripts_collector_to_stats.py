from get_vacanciesID_by_API import collect_vacancies_id
from get_vacancies_data_from_IDs import collect_vacancies_info
from words_list import collect_words_from_vacancies_info
import io
from datetime import datetime


PATH = './rc/find_results/'
TIMEOUT = 0.3


def logging(logs: io.TextIOWrapper, text: str):
    print(datetime.now(), text)
    logs.write(str(datetime.now()) + ': ' + text + '\n')


if __name__ == '__main__':
    logs = open('script_collector_to_stats.log', 'a', encoding='u8')
    file_requests = open('rc/requests.txt', encoding='u8')
    for request in file_requests:
        if not request.replace(' ', ''):
            continue
        logging(logs, 'запрос: ' + request)
        request = request[:-1]
        dirpath = PATH + request
        collect_vacancies_id(text=request, path=dirpath, timeout=TIMEOUT)
        logging(logs, 'collected vacancies id of ' + request)
        collect_vacancies_info(path=dirpath, timeout=TIMEOUT)
        logging(logs, 'collected vacancies info of ' + request)
        collect_words_from_vacancies_info(path=dirpath)
        logging(logs, 'collected words of ' + request + '\n')

    file_requests.close()
    logs.close()