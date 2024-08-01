"""
Модуль для работы с фотографиями из ВКонтакте и их загрузки на Yandex Disk и Google Drive.

Этот модуль предоставляет функции для:
- Получения токенов для доступа к API ВКонтакте и Yandex Disk из конфигурационного файла.
- Извлечения URL фотографий из заданного альбома пользователя ВКонтакте.
- Загрузки фотографий из ВКонтакте на локальный компьютер.
- Загрузки фотографий на Yandex Disk.
- Загрузки фотографий из локальной папки в Google Drive.

Основные функции:
- print_progress_bar: Отображает прогресс загрузки.
- get_tokens: Читает токены из конфигурационного файла.
- get_photo_urls: Получает URL фотографий из ВКонтакте по имени пользователя и количеству.
- upload_to_yandex_disk: Загружает фотографии на Yandex Disk.
- download_to_local: Скачивает фотографии с ВКонтакте на локальный компьютер.
- upload_to_google_drive: Загружает фотографии из локальной папки на Google Drive.

Перед использованием модуля необходимо установить соответствующие библиотеки и настроить API для доступа к ВКонтакте, Yandex Disk и Google Drive.
"""
import time
import progressbar
import downloader_vk
import uploader_yd
import uploader_gd
import configparser
from typing import Tuple, Dict, Any

def print_progress_bar(iterations: int) -> None:
    """
    Создает и отображает прогресс бар.

    Args:
        iterations (int): Количество итераций для отображения в прогресс баре.
    """
    bar = progressbar.ProgressBar()
    for _ in bar(range(iterations)):
        time.sleep(0.001)
    bar.finish()

def get_tokens(file_name: str = "settings.ini") -> Tuple[str, str]:
    """
    Читает токены из конфигурационного файла.

    Args:
        file_name (str): Имя файла конфигурации.

    Returns:
        Tuple[str, str]: Токен VK и токен Yandex Disk.
    """
    config = configparser.ConfigParser()
    config.read(file_name)
    vk_token = config["TOKENS"]["vk_token"]
    ya_token = config["TOKENS"]["token_ya"]
    return vk_token, ya_token

def get_photo_urls(count: int = 5) -> Tuple[Dict[str, str], str, str]:
    """
    Получает URL фотографий из VK.

    Args:
        count (int): Количество фотографий для получения.

    Returns:
        Tuple[Dict[str, str], str, str]: Словарь URL фотографий, токен VK и ID пользователя.
    """
    vk_token = get_tokens()[0]
    vk_id = downloader_vk.DownloaderVK.get_id(screen_name, vk_token)
    downloader = downloader_vk.DownloaderVK(vk_token, vk_id)
    photo_urls = downloader.get_photos(count)
    return photo_urls, vk_token, vk_id

def upload_to_yandex_disk(count: int, folder_name: str) -> None:
    """
    Загружает фотографии на Yandex Disk.

    Args:
        count (int): Количество фотографий для загрузки.
        folder_name (str): Имя папки на Yandex Disk.
    """
    ya_token = get_tokens()[1]
    uploader = uploader_yd.UploaderYD(ya_token, folder_name)
    uploader.folder_creation()
    
    photo_urls = get_photo_urls(count)[0]
    for counter, (name, link) in enumerate(photo_urls.items(), start=1):
        uploader.upload(name, link)
        print(f'Загружено {counter} фото на YandexDisk, {name} в папке {folder_name}')
        print_progress_bar(counter)

def download_to_local(count: int, folder_name: str) -> None:
    """
    Загружает фотографии с VK на локальный компьютер.

    Args:
        count (int): Количество фотографий для загрузки.
        folder_name (str): Имя папки для загрузки.
    """
    vk_token, vk_id = get_photo_urls()[1], get_photo_urls()[2]
    downloader = downloader_vk.DownloaderVK(vk_token, vk_id, folder_name)
    downloader.download_to_pc(count)

def upload_to_google_drive(folder_name: str) -> None:
    """
    Загружает фотографии из локальной папки в Google Drive.

    Args:
        folder_name (str): Имя папки на Google Drive.
    """
    uploader = uploader_gd.UploaderGD()
    folder_id = uploader.folder_creation(folder_name)
    uploader.upload(folder_id, folder_name)

def optional():
    print('Загрузить фотографии на жёсткий диск? Yes/y/да')
    answer = input()
    if answer.lower() == 'yes' or answer.lower() == 'да' or answer.lower() == 'y':
        download_to_local(photos_count, folder_name) # Локальная загрузка (опционально)
    else:
        pass
    print(f'Загрузить фотографии на Google Drive из папки {folder_name}? Yes/y/да')
    answer = input()
    if answer.lower() == 'yes' or answer.lower() == 'да' or answer.lower() == 'y':
        upload_to_google_drive(folder_name) # Загрузка фото на Google Drive всех файлов из папки folder_name
    else:
        pass
    print('Работа программы завершена!')

if __name__ == '__main__':
    screen_name = str(input('Введите никнейм пользователя или id: '))
    folder_name = str(input('Введите имя папки: '))
    photos_count = int(input('Введите количество фотографий для загрузки: '))
    upload_to_yandex_disk(photos_count, folder_name) # Загрузка фото на ЯД
    optional()