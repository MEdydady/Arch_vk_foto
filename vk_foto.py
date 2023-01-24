import json
import time

import requests


class VkUserFoto:
    url = "https://api.vk.com/method/"

    # Инициализация
    def __init__(self, token, version):
        self.params = {"access_token": token, "v": version}

    # Функция  возвращает все фотографии профиля 
    def search_vk_foto(self, vk_id=None):
        search_foto_url = self.url + "photos.get"
        search_foto_params = {
            "user_id": vk_id,
            "extended": "1",
            "album_id": "profile",
            "count": 300,
            "photo_sizes": "0",
        }

        req = requests.get(
            search_foto_url, params={**self.params, **search_foto_params}
        ).json()

        return req["response"]["items"]

    # Функция возвращает список фотографий в нужной нам форме 
    def create_json(self):
        list_foto = []
        dict_foto = {}
        size_dict = {
            "s": 1,
            "m": 2,
            "o": 3,
            "p": 4,
            "q": 5,
            "r": 6,
            "x": 7,
            "y": 8,
            "z": 9,
            "w": 10,
        }
        count = 0
        tr = self.search_vk_foto()
        for x in tr:
            dict_foto = {}
            name_file_date_unix = x["date"]
            name_file_date = time.strftime(
                "%m%d%Y_%H%M%S", time.gmtime(name_file_date_unix) 
            ) # Перевод даты  
           
            file_url = max(x["sizes"], key=lambda x: size_dict[x["type"]])  # Выбираю ссылки  на фотографии максимального размера
            
            # Создаю список в нужной мне форме
            file = file_url["url"]
            dict_foto["name_like"] = x["likes"]["count"]
            dict_foto["name_date"] = name_file_date
            dict_foto["link"] = file
            dict_foto["type"] = file_url["type"]
            list_foto.append(dict_foto)
            count = count + 1

        # Создаю json с ссылками на фотографии и параметрами профиля  для  восприятия )
        with open(
            "photo.json", "w", encoding="utf-8"
        ) as f:  # Сохраняю ответ в файл json
            json.dump(list_foto, f, ensure_ascii=False, indent=4)

        return list_foto, count
