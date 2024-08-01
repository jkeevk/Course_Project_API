"""
Модуль для работы с фотографиями из ВКонтакте.

Этот модуль предоставляет класс `DownloaderVK`, который позволяет загружать 
фотографии пользователей из ВКонтакте с использованием VK API. Класс предоставляет 
возможности для получения идентификатора пользователя по имени, извлечения фотографий 
и их скачивания на локальный компьютер.

Класс `DownloaderVK` предлагает следующие функции:
- Получение ID пользователя ВКонтакте из его имени.
- Извлечение фотографий пользователя из его профиля.
- Скачивание фотографий на локальный компьютер и сохранение их в указанной папке.

Основные методы:
- `__init__`: Инициализирует экземпляр класса с токеном доступа и ID пользователя.
- `get_id`: Получает ID пользователя ВКонтакте по его имени (screen_name).
- `get_photos`: Запрашивает фотографии у пользователя, возвращая словарь с именами 
  файлов и соответствующими URL фотографий.
- `download_to_pc`: Скачивает указанное количество фотографий на локальный компьютер 
  в указанную папку, создавая ее при необходимости.
"""
import requests
import json
import os
import sys
import json_dumper
from datetime import datetime
from typing import Dict, Any

class DownloaderVK:
    """Класс для работы с фотографиями из ВКонтакте"""
    def __init__(self, vk_token: str, vk_id: str, folder_name=None) -> None:
        """
        Инициализирует экземпляр DownloaderVK.

        Args:
            vk_token (str): Токен доступа к VK API.
            vk_id (str): ID пользователя или сообщества VK.
        """
        self.vk_token = vk_token
        self.vk_id = vk_id
        self.folder_name = folder_name

    @classmethod
    def get_id(cls, screen_name: str, vk_token: str) -> str:
        """
        Получает ID из screen_name.

        Args:
            screen_name (str): Имя пользователя или идентификатор.
            vk_token (str): Токен доступа к VK API.

        Returns:
            str: ID пользователя VK.
        """
        if screen_name.isdigit():
            vk_id = screen_name
        else:
            url = 'https://api.vk.com/method/utils.resolveScreenName'
            params = {
                'screen_name': screen_name,
                'access_token': vk_token,
                'v': '5.131'
            }
            response = requests.get(url=url, params=params).json()
            vk_id = response['response']['object_id']
        return vk_id

    def get_photos(self, count: int = 5, offset: int = 0) -> Dict[str, str]:
        """
        Получает фотографии пользователя из VK.

        Args:
            count (int): Количество фотографий для получения.
            offset (int): Смещение для постраничного получения.

        Returns:
            Dict[str, str]: Словарь с именами файлов и URL фотографий.
        """
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.vk_id,
            'album_id': 'profile',
            'access_token': self.vk_token,
            'v': '5.131',
            'extended': '1',
            'photo_sizes': '1',
            'count': count,
            'offset': offset
        }
        response = requests.get(url=url, params=params)
        if 'error' in response.json():
            print('Во время загрузки произошла ошибка.\nВозможно, пользователь заблокирован, удалён или ещё не создан.\nУбедитесь в правильности введённых данных и удостоверьтесь, что альбом не защищён настройками приватности.')
            sys.exit()

        json_dump = json_dumper.DumpJSON()
        json_dump.create_json()

        photo_dict = {}
        all_photos_info = response.json()
        total_photos = len(all_photos_info['response']['items'])

        for i in range(total_photos):
            max_height = 0
            photo_url = ''
            size = ''

            for photo in all_photos_info['response']['items'][i]['sizes']:
                if photo['height'] >= max_height:
                    max_height = photo['height']
                    photo_url = photo['url']
                    size = photo['type']

            likes_count = all_photos_info['response']['items'][i]['likes']['count']

            if f"{likes_count}.jpg" not in photo_dict:
                photo_dict[f"{likes_count}.jpg"] = photo_url
                data = {
                    "file_name": f"{likes_count}.jpg",
                    "size": size
                }
                json_dump.add_to_json(data)
            else:
                unix_time = all_photos_info['response']['items'][i]['date']
                dt = datetime.utcfromtimestamp(unix_time)
                new_file_name = f"{likes_count}_{dt.day}.{dt.month}.{dt.year}.jpg"
                photo_dict[new_file_name] = photo_url
                data = {
                    "file_name": f"{likes_count}.jpg",
                    "size": size
                }
                json_dump.add_to_json(data)

        return photo_dict

    def download_to_pc(self, count: int) -> None:
        """
        Скачивает фотографии на локальный компьютер.

        Args:
            count (int): Количество фотографий для скачивания.
        """
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)  # Создаем папку для скачивания

        for counter, (file_name, photo_url) in enumerate(self.get_photos(count).items(), start=1):
            with open(f'{self.folder_name}/{file_name}', 'wb') as file:
                image = requests.get(photo_url)
                file.write(image.content)
                print(f'Скачано {counter} фото из VK, файл: {file_name}')