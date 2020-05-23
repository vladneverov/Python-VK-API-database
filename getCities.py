import time
import math
from termcolor import colored
import requests
from configs.config import *
from configs.DBConfig import *

def main():
    # Удалить таблицу "cities" если существует
    cursor.execute("DROP TABLE IF EXISTS cities")

    # Создать таблицу "cities" если не существует
    cursor.execute("CREATE TABLE IF NOT EXISTS cities (id INT(11) PRIMARY KEY, title VARCHAR(255), \
                        area VARCHAR(255), region VARCHAR(255), region_id INT(11), country_id INT(11))")

    # Выбрать все регионы с сортировкой по полю country_id
    cursor.execute("SELECT * FROM regions ORDER BY country_id")
    regions = cursor.fetchall()

    def getCities(country_id, region_id, offset):
        r = requests.get('https://api.vk.com/method/database.getCities', params={
            'country_id': country_id, 'region_id': region_id, 'need_all': 1, 'offset': offset, 'lang': 'ru', 'count': 1000, 'v': 5.103, 'access_token': token
        }, proxies=proxies)

        return r.json()["response"]["items"]

    for region_id, region in enumerate(regions, start=1):

        # Получить города по id страны и id региона
        cities = getCities(region[2], region[0], 0)
        countCities = len(cities)

        if countCities > 999:
           print(countCities, colored("Городов больше 1000!", "blue"))
           pages = math.ceil(countCities / 999)
           print("Всего страниц " + str(pages))

           offset = 1
           while (offset < pages):
               offset += 1

               print("Получаем страницу " + str(offset))
               cities = getCities(region[2], region[0], offset)

               for city in cities:

                   # get() позволяет если нет такого ключа, установить ''
                   # Добавить в базу
                   sql = "INSERT INTO cities (id, title, area, region, region_id, country_id) VALUES (%s, %s, %s, %s, %s, %s)"
                   val = (city["id"], city["title"], city.get('area', ''), city.get('region', ''), region[0], region[2])
                   cursor.execute(sql, val)
                   db.commit()

                   time.sleep(1)
        else:
            for city in cities:
                # get() позволяет если нет такого ключа, установить ''
                # Добавить в базу
                sql = "INSERT INTO cities (id, title, area, region, region_id, country_id) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (city["id"], city["title"], city.get('area', ''), city.get('region', ''), region[0], region[2])
                cursor.execute(sql, val)
                db.commit()

                time.sleep(1)

if __name__ == '__main__':
    main()