import requests
import re

from pprint import pprint
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient

# Все как раньше
num_area = '4'
wanted_profession = 'povar'
main_link = 'https://www.superjob.ru'
vacancies = []
# Счетчик страниц
page = 1

search_link = f'{main_link}/vakansii/{wanted_profession}.html?geo%5Bt%5D%5B0%5D={num_area}'

# Для быстроты ограничился только двумя страницами
while page < 3:
    response = requests.get(search_link).text 
    print('While:', page)
    html = bs(response,'lxml')

    vacancy_block = html.find_all('div',{'class':'QiY08 LvoDO'})

    for i in range(0, len(vacancy_block), 2):

        vacancy_dict = {}

        vacancy_dict['profession'] = vacancy_block[i].find('div', {'class': '_3mfro'}).getText()
        vacancy_dict['link'] = main_link + vacancy_block[i].find('a', {'class': 'icMQ_'}).get('href')
        salary = (vacancy_block[i].find('span', {'class': 'f-test-text-company-item-salary'}).getText()).split('—')
        # Отсортировал все зарплаты и выбрал только числа
        if len(salary) == 2:
            vacancy_dict['salary_min'] = int(''.join(re.findall('\d', salary[0])))
            vacancy_dict['salary_max'] = int(''.join(re.findall('\d',salary[1])))
        elif len(salary) == 1 and re.findall('до\s', salary[0]):
            vacancy_dict['salary_min'] = 0
            vacancy_dict['salary_max'] = int(''.join(re.findall('\d', salary[0])))
        elif len(salary) == 1 and re.findall('По договорённости', salary[0]):
            vacancy_dict['salary_min'] = 0
            vacancy_dict['salary_max'] = 0
        else:
            vacancy_dict['salary_min'] = int(''.join(re.findall('\d', salary[0])))
            vacancy_dict['salary_max'] = 0
        # Поскольку других валют не обнаружилось, то я и не стал их выбирать
        vacancy_dict['currency'] = '₽'
        vacancies.append(vacancy_dict)

    page += 1
    # Перелистываем страницу
    search_link = f'{search_link}&page={page}'

# При установке Mongo на Mac OS Catalina имеются особенности. Информации в интернете мало.
# Только на англоязычных сайтах. Поэтому поделюсю. Может пригодится.

# 1. Если не установлен, то устанавливаем Homebrew (пактный менеджер для MAC)

# Дальше по порядку выполняем следующие команды
# 2. brew tap mongodb/brew
# 3. brew install mongodb-community

# Создаем директорию для Mongo
# 4. sudo mkdir -p /Sistem/Volumes/Data/data/db
# 5. sudo chown -R `id - un` /Sistem/Volumes/Data/data/db

# Проверка установки
# mongo --version

# Запуск
# sudo mongod --dbpath /Sistem/Volumes/Data/data/db

# Чтобы не писать каждый раз такую строчку, можно создать псевдоним
# alias mongod="sudo mongod --dbpath /Sistem/Volumes/Data/data/db"
# и запускать командой mongod

client  = MongoClient('localhost',27017)
db = client['work_sj']
work_sj = db.work_sj

# Предварительно удалял данные, чтобы не заполнять БД при отладке
work_sj.remove()
work_sj.insert_many(vacancies)

# Вывод всей БД
# objects = work_sj.find()
# for obj in objects:
#     pprint(obj)


def search_salary(min_currency):
    all_salafy = work_sj.find({'salary_min': {'$gt' : min_currency}})
    for salary in all_salafy:
        print('*' * 52)
        pprint(salary)

search_salary(40000)

# Как сделать добавление только тех вакансий, которых нет, не сообразил.


