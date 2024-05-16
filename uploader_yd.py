import requests


class Uploader_YD:
    
    def __init__(self, token_ya, folder_name):
        self.token_ya = token_ya
        self.folder_name = folder_name

    def folder_creation(self): # создаём папку
        url = f'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = {'Content-Type': 'application/json',
                    'Authorization': f'OAuth {self.token_ya}'}
        params = {'path': f'{self.folder_name}',
                    'overwrite': 'false'}
        response = requests.put(url=url, headers=headers, params=params)

    def upload(self, filename, curl):
        url = f'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json',
                        'Authorization': f'OAuth {self.token_ya}'}
        params = {'path': f'{self.folder_name}/{filename}',
                        'overwrite': 'true'}
        
        response = requests.get(url=url, headers=headers, params=params) # получение ссылки на загрузку
        href = response.json().get('href')

        uploader = requests.put(href, curl)
        
