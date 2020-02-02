from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests

# На HH я так и не смог получить ответ со странички. Всегда ошибка 404.
# Сделал только для superjob

# Полная ссылка для поиска 'https://www.superjob.ru/vakansii/povar.html?geo%5Bt%5D%5B0%5D=4'
num_area = '4'
wanted_profession = 'povar'
main_link = 'https://www.superjob.ru'

# Со страницами я не понял, как определить последнюю или их число, поэтому ограничился одной страницей

response = requests.get(f'{main_link}/vakansii/{wanted_profession}.html?geo%5Bt%5D%5B0%5D={num_area}').text
html = bs(response,'lxml')

# Находим все div-ы с информацией о вакансиях
vacancy_block = html.find_all('div',{'class':'QiY08 LvoDO'})

print(len(vacancy_block))
# Я не понял, почему у меня данные записались 2 раза. 
# Потратил N -ное количество времени, но не понял.
# Двух одинаковых div-ов с классом QiY08 LvoDO я не нашел.
# Поэтому сделал костыль в виде цикла с шагом 2.
# Это, конечно, плохо, но я надеюсь, что BeautifulSoup заменю на Scrapy.
# Обещаю с ним разобраться досконально.
vacancies = []
pattern_min = '/d'

for i in range(0, len(vacancy_block), 2):

    vacancy_dict = {}

    vacancy_dict['profession'] = vacancy_block[i].find('div', {'class': '_3mfro'}).getText()
    vacancy_dict['link'] = main_link + vacancy_block[i].find('a', {'class': 'icMQ_'}).get('href')
    vacancy_dict['salary'] = (vacancy_block[i].find('span', {'class': 'f-test-text-company-item-salary'}).getText()).split('—')

    vacancies.append(vacancy_dict)


print('*' * 52)
print(vacancies[0]['profession'])

for vacancy in vacancies:
    profession = vacancy['profession']
    min_salary = vacancy['salary'][0]
    if len(vacancy['salary']) == 2:
        max_salary = vacancy['salary'][1]
    else:
        max_salary = ' Не указана'
    link_vacancy = vacancy['link']

    print(f'Профессия: {profession}.\nМинимальная зарплата:   {min_salary}.\nМаксимальная зарплата: {max_salary}.\nСсылка: {link_vacancy}')
    print()

