# 1. Создать приложение VK Standalone
# 2. Записать ID приложения
# 3. Получить по ссылке токен и разрешить права
# Можно и сервисный ключ приложения, но там глюки

# ID приложения	7350440
# для Standalone приложения - redirect_uri=https://oauth.vk.com/blank.html
# {TOKEN} = https://oauth.vk.com/authorize?client_id={APP_ID}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,photos,audio,video,docs,notes,pages,status,wall,groups,notifications,offline&response_type=token
# https://api.vk.com/method/database.getCountries?access_token={TOKEN}&need_all=1&v=5.103