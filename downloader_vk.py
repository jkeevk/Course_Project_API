import requests, json, os
from datetime import datetime
from json_dumper import add_to_json


class Downloader_VK:

    def __init__(self, vk_token: str, vk_id):
        self.vk_token = vk_token
        self.vk_id = vk_id

    @classmethod
    def get_id(self, screen_name, vk_token: str): # получение id из screen_name
        for letter in screen_name:
            if not letter.isdigit():
                url = 'https://api.vk.com/method/utils.resolveScreenName'
                params = {'screen_name': screen_name,
                    'access_token': vk_token,
                    'v': '5.131'}
                res = requests.get(url=url, params=params).json()
                vk_id = res['response']['object_id']
                return vk_id
            else:
                vk_id = screen_name
                return vk_id


    def get_photos(self, count=5, offset=0):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.vk_id,
                      'album_id': 'profile',
                      'access_token': self.vk_token,
                      'v': '5.131',
                      'extended': '1',
                      'photo_sizes': '1',
                      'count': count,
                      'offset': offset
                      }
        res = requests.get(url=url, params=params)
        all_dict = {} # в словарь значения 'название файла':'ссылка'
        all_photoes_info = res.json()
        all_photo_count = len(all_photoes_info['response']['items'])
        for i in range(all_photo_count):
            max_height = 0
            for photo in (all_photoes_info['response']['items'][i]['sizes']): # поиск самой большой картинки
                if photo['height'] >= max_height: 
                    max_height = photo['height']
                    size = photo['type']
                if max_height == photo['height']:
                    url = photo['url']
                    size = photo['type']
            likes_count = all_photoes_info['response']['items'][i]['likes']['count']
            if f"{likes_count}.jpg" not in all_dict.keys(): # проверка на одинаковое количество лайков
                all_dict[f"{likes_count}.jpg"] = photo['url']
                data = {
                    "file_name": f"{likes_count}.jpg",
                    "size": size} 
                add_to_json(data)
                
            else:
                unix_time = all_photoes_info['response']['items'][i]['date']
                dt = datetime.utcfromtimestamp(unix_time) # перевод времени в читаемую дату
                all_dict[f"{likes_count}_{dt.day}.{dt.month}.{dt.year}.jpg"] = photo['url']
                data = {
                    "file_name": f"{likes_count}.jpg",
                    "size": size}
                add_to_json(data)
                
        return all_dict

    def download_on_pc(self, count): # скачивание файлов локально

        if not os.path.exists('VK Images'): # создаем папку для скачивания
            os.mkdir('VK Images')
                    
        counter = 1 
        for file_name, photo_url in self.get_photos(count).items(): # загружаем файлы в папку
            with open('VK Images/%s' % f'{file_name}', 'wb') as file:
                image = requests.get(photo_url)
                file.write(image.content)
                print(f'Скачано {counter} фото из VK, файл: {file_name}')
                counter += 1
            
