import copy
import json
from datetime import datetime
import io


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


string = '16:22:30,000000'
time_test = datetime.strptime(string, '%H:%M:%S,%f')
print(time_test)


logs = open('results.log', 'a')
print(type(logs), isinstance(logs, io.TextIOWrapper))

print(len(4562))


