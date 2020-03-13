# 1. Создать приложение VK Standalone
# 2. Записать ID приложения
# 3. Получить по ссылке токен и разрешить права
# Можно и сервисный ключ приложения, но там глюки

# ID приложения	7350440
# для Standalone приложения - redirect_uri=https://oauth.vk.com/blank.html
# {TOKEN} = https://oauth.vk.com/authorize?client_id={APP_ID}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,photos,audio,video,docs,notes,pages,status,wall,groups,notifications,offline&response_type=token
# https://api.vk.com/method/database.getCountries?access_token={TOKEN}&need_all=1&v=5.103




















import requests

token= '23ac56974452faa4d444bc64f066194d283acdad30b2038a442e6abe0566a1dd85fa4334d2df8008a5b39'
proxies = {
    'http': 'http://200.73.128.5:8080',
    'https': 'http://200.73.128.5:8080',
}
 
def main():
    r = requests.get('https://api.vk.com/method/database.getCountries', params={
        'need_all': 1,'v': 5.103,'access_token': token
    }, proxies=proxies)
    countries = r.json()["response"]["items"]

    for country in countries:
        print(country["title"])
 
if __name__ == '__main__':
    main()