import time

import vk_foto
import ya_put_foto

# Читаем токен для ВК
with open("tokenvk.txt", "r") as file_object:
    tokenvk = file_object.read().strip()

# Читаем токен для Yandex
with open("tokenya.txt", "r") as file_object:
    tokenya = file_object.read().strip()


# Инициализация класса и вызов  функции, которая возвращает список фотографий
vk_client = vk_foto.VkUserFoto(tokenvk, "5.131")
photo_list_ya, count = vk_client.create_json()

user_count = int(input(f'Всего найдено {count} фотографий, какое количество загрузить? '))
folder_name = input("Введите имя папки в яндекс диске ")



# Инициализация класса и вызов  функции, которая создает папку и записывает фотографии на диск.
start = ya_put_foto.YaPutFoto(tokenya, photo_list_ya)  
start.create_folder(folder_name)

# Проверка на количество фотографий, если пользователь введет больше, то будет скачено 5 фотографий.
if user_count > count:
    start.upload_from_internet(folder_name) 
else:    
    start.upload_from_internet(folder_name, user_count) 
