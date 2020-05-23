import sys
import time
from termcolor import colored
import requests
from configs.config import *
from configs.DBConfig import *

def main():
    # Удалить таблицу "regions" если существует
    cursor.execute("DROP TABLE IF EXISTS regions")

    # Создать таблицу "regions" если не существует
    cursor.execute("CREATE TABLE IF NOT EXISTS regions (region_id INT(11) PRIMARY KEY, title VARCHAR(255), country_id INT(11))")

    # Выбрать все страны
    cursor.execute("SELECT * FROM countries")
    countries = cursor.fetchall()

    def getRegions(country_id):
        r = requests.get('https://api.vk.com/method/database.getRegions', params={
            'country_id': country_id, 'lang': 'ru', 'count': 1000, 'v': 5.103, 'access_token': token
        }, proxies=proxies)
        
        return r.json()["response"]["items"]

    listRegions = []

    for country_id, country in enumerate(countries, start=1):
      
        # Получить регионы по id страны
        regions = getRegions(country_id)
        countRegions = len(regions)
 
        if countRegions <= 1000:
           for region in regions:

               # Записать списком из кортежей для sql запроса
               listRegions.append( (region["id"], region["title"], country_id) )
        else:
            print(countRegions, colored("Ошибка, регионов больше 1000!", "red"))
            sys.exit()

        print(countRegions, colored("Регионов добавлено.", "green"))
        time.sleep(1)

    listSortRegions = sorted(listRegions, key=lambda country_id: country_id[2])

    # Добавить в базу
    sql = "INSERT INTO regions (region_id, title, country_id) VALUES (%s, %s, %s)"
    cursor.executemany(sql, listSortRegions)
    db.commit()

    print(cursor.rowcount, colored("Регионы были успешно добавлены!", "green"))

if __name__ == '__main__':
    main()