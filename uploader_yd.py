"""
Модуль для загрузки файлов на Яндекс.Диск.

Этот модуль предоставляет класс `UploaderYD`, который позволяет загружать файлы
на Яндекс.Диск. Класс также предоставляет функциональность для создания новых папок
на диске и управления файлами внутри них.

Класс `UploaderYD` предлагает следующие функции:
- Инициализация с токеном доступа и именем папки для загрузки файлов.
- Создание новой папки на Яндекс.Диске, если она не существует.
- Загрузка файлов в указанную папку на Яндекс.Диске.

Основные методы:
- `__init__`: Инициализирует экземпляр класса с токеном и именем папки.
- `folder_creation`: Создает новую папку на Яндекс.Диске, если она не существует.
- `upload`: Загружает файл на Яндекс.Диск, предоставляя возможность указать 
  имя файла и его содержимое.
"""
import requests
from typing import Union


class UploaderYD:
    """Класс для загрузки файлов на Яндекс.Диск."""    
    def __init__(self, token_ya: str, folder_name: str) -> None:
        """
        Инициализирует класс Uploader_YD с токеном и именем папки.

        Args:
            token_ya (str): Токен доступа к Яндекс.Диску.
            folder_name (str): Имя папки для загрузки файлов.
        """
        self.token_ya = token_ya
        self.folder_name = folder_name

    def folder_creation(self) -> None:
        """Создает новую папку на Яндекс.Диске, если она не существует."""
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token_ya}'
        }
        params = {
            'path': self.folder_name,
            'overwrite': 'false'
        }
        response = requests.put(url=url, headers=headers, params=params)
        
        if response.status_code == 201:
            print(f"Папка '{self.folder_name}' успешно создана.")
        elif response.status_code == 409:
            print(f"Папка '{self.folder_name}' уже существует.")
        else:
            print(f"Ошибка при создании папки: {response.text}")


    def upload(self, filename: str, curl: Union[bytes, str]) -> bool:
        """
        Загружает файл на Яндекс.Диск.

        Args:
            filename (str): Имя файла, который нужно загрузить.
            curl (str): Данные файла, которые будут загружены.

        Returns:
            bool: Успешность загрузки файла.
        """
        url = f'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token_ya}'
        }
        params = {
            'path': f'{self.folder_name}/{filename}',
            'overwrite': 'true'
        }
        
        
        response = requests.get(url=url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Ошибка получения ссылки для загрузки: {response.text}")
            return False
        
        href = response.json().get('href')
        uploader = requests.put(href, curl)

        if uploader.status_code == 201:
            print(f"Файл '{filename}' успешно загружен.")
            return True
        else:
            print(f"Ошибка при загрузке файла: {uploader.text}")
            return False
