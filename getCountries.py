import sys
from termcolor import colored
import requests
from configs.config import *
from configs.DBConfig import *
 
def main():
    # Создать базу "vkdb" если не существует
    cursor.execute("CREATE DATABASE IF NOT EXISTS vkdb")

    # Удалить таблицу "countries" если существует
    cursor.execute("DROP TABLE IF EXISTS countries")

    # Создать таблицу "countries" если не существует
    cursor.execute("CREATE TABLE IF NOT EXISTS countries (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))")

    listCountries = []
    listCountries.reverse()

    def getCountries():
        r = requests.get('https://api.vk.com/method/database.getCountries', params={
            'need_all': 1, 'lang': 'ru', 'count': 1000, 'v': 5.103, 'access_token': token
        }, proxies=proxies)
        
        return r.json()["response"]["items"]
    
    countries = getCountries()
    lenCountries = len(countries)

    file = open('txtFiles/countries.txt', 'w', encoding='utf-8')

    for index, country in enumerate(countries):
        
        # Записать списком из кортежей для sql запроса
        listCountries.append( (country["title"], ) )

        # Если это последняя строка
        # Убрать перенос \n
        if index == lenCountries - 1:
           file.write(country["title"])
        else:
           # Записать в txt файл
           file.write(country["title"] + "\n")

    file.close()

    # Добавить все страны в базу
    sql = "INSERT INTO countries (title) VALUES (%s)"
    cursor.executemany(sql, listCountries)
    db.commit()

    print(cursor.rowcount, colored("Страны были успешно добавлены!", "green"))
 
if __name__ == '__main__':
    main()