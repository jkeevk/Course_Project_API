import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class Uploader_GD:

    def __init__(self):
        gauth = GoogleAuth()
        self.drive = GoogleDrive(gauth)

    def folder_creation(self, folder_name): # создание папки в Google Drive
        folder_metadata = {'title' : folder_name, 'mimeType' : 'application/vnd.google-apps.folder'}
        folder = self.drive.CreateFile(folder_metadata)
        folder.Upload()
        folderid = folder['id']
        return folderid

    def upload(self, folderid):
        if not os.path.exists('VK Images'):
            os.mkdir('VK Images')
        directory = 'VK Images/' # загрузка фотографий в папку
        for f in os.listdir(directory):
            file_name = f
            file_metadata = {'title': file_name, "parents": [{"id": folderid, "kind": "drive#childList"}]}
            folder = self.drive.CreateFile(file_metadata)
            folder.SetContentFile(f'{directory}/{file_name}')
            folder.Upload()


