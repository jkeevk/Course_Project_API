"""
Модуль для загрузки файлов в Google Drive.

Этот модуль предоставляет класс `UploaderGD`, который позволяет загружать файлы
из локальной папки в Google Drive. Класс также предоставляет функциональность для
создания новых папок в Google Drive и управления файлами внутри них.

Класс `UploaderGD` предлагает следующие функции:
- Аутентификация пользователя с использованием GoogleAuth для доступа к Google Drive.
- Создание новой папки в Google Drive с заданным именем.
- Загрузка локальных файлов в указанную папку Google Drive.

Основные методы:
- `__init__`: Инициализирует экземпляр класса и аутентифицирует пользователя с помощью GoogleAuth.
- `folder_creation`: Создает новую папку в Google Drive и возвращает ее идентификатор.
- `upload`: Загружает файлы из указанной локальной папки в папку Google Drive,
  проверяя наличие локальной папки перед загрузкой и обрабатывая ситуации, когда папка отсутствует.
"""
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class UploaderGD:
    """Класс для загрузки файлов в Google Drive."""
    def __init__(self) -> None:
        """
        Инициализирует класс Uploader_GD, аутентифицируя пользователя
        и создавая объект GoogleDrive.
        """
        gauth = GoogleAuth()
        self.drive = GoogleDrive(gauth)

    def folder_creation(self, folder_name: str) -> str:
        """
        Создает папку в Google Drive.

        Args:
            folder_name (str): Имя папки, которую необходимо создать.

        Returns:
            str: Идентификатор созданной папки.
        """
        folder_metadata = {'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
        folder = self.drive.CreateFile(folder_metadata)
        folder.Upload()
        folderid = folder['id']
        return folderid

    def upload(self, folderid: str, folder_name:str) -> None:
        """
        Загружает файлы из локальной папки в указанную папку Google Drive.

        Args:
            folderid (str): Идентификатор папки в Google Drive, куда будут загружены файлы.
            folder_name:str : Имя папки, откуда загружать фото.
        Raises:
            FileNotFoundError: Если локальная папка не найдена.
        """
        if not os.path.exists(folder_name):
            raise FileNotFoundError(f"Папка '{folder_name}' не найдена. Убедитесь, что она существует.")

        for file_name in os.listdir(folder_name):
            file_metadata = {
                'title': file_name,
                "parents": [{"id": folderid, "kind": "drive#childList"}]
            }
            file_path = os.path.join(folder_name, file_name)
            file = self.drive.CreateFile(file_metadata)
            file.SetContentFile(file_path)
            file.Upload()
            print(f'Файл {file_name} загружен')

        print(f"Файлы успешно загружены в папку {folder_name} с ID: {folderid}.")


