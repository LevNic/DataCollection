import requests
import json
from pprint import pprint

# Пример из Яндекса
# lon=<долгота>
#  lat=<широта>
# GET https://api.weather.yandex.ru/v1/forecast?

api_key = '6e5e6140-67a0-4ea1-83d5-147f408ae9b8'
lat = 55.75396
lon = 37.620393

url = f'https://api.weather.yandex.ru/v1/forecast?lat={lat}&lon={lon}'
key = {'X-Yandex-API-Key': api_key}


response = requests.get(url, headers=key)
data = json.loads(response.text)
pprint(data)
