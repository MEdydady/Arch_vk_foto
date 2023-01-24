import json
import pprint
import time

import requests

from progress.bar import IncrementalBar


class YaPutFoto:

    host = "https://cloud-api.yandex.net/"

    def __init__(self, token, photo_list_ya):
        self.token = token
        self.data = photo_list_ya

    def get_headers(self):
        return {
            "Content-Type": "applicac:\tion/json",
            "Authorization": f"OAuth {self.token}",
        }

    #  Получение ссылки для загрузки
    def get_upload_link(self, file_name):
        uri = "v1/disk/resources/upload/"
        url = self.host + uri
        params = {"path": f"/{file_name}"}
        response = requests.get(url, headers=self.get_headers(), params=params)
        print(response.json())
        return response.json()["href"]

    # Загрузка фотографий
    def upload_from_internet(self, folder_name, count=5):
        uri = "v1/disk/resources/upload/"
        url = self.host + uri
        bar = IncrementalBar("Processing", max=count)
        l = 0
        good_list = []  # пустой список для  результирующего json  файла

        for i in self.data:
            good_dic = {}
            if (
                l >= count
            ):  # Проверка количество запросов на скачку , если пользователь введет больше число, чем фотографий.
                break
            bar.next()
            time.sleep(0.33)
            params = {"path": f"/{folder_name}/{i['name_date']}", "url": i["link"]}
            response = requests.post(url, headers=self.get_headers(), params=params)
            l += 1

            # Записываю в json  если ответ пришёл положительный
            if response.status_code == 202 or response.status_code == 200:
                good_dic["file_name"] = i.get("name_date")
                good_dic["size"] = i.get("type")
                good_list.append(good_dic)

        bar.finish()

        with open(
            "photo_ok.json", "w", encoding="utf-8"
        ) as f:  # Сохраняю ответ в файл json
            json.dump(good_list, f, ensure_ascii=False, indent=4)

    # Создание папки
    def create_folder(self, name_fol):
        uri = "v1/disk/resources/"
        url = self.host + uri
        params = {"path": f"/{name_fol}"}
        response = requests.put(url, headers=self.get_headers(), params=params)
