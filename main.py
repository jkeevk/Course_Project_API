import time, progressbar
import downloader_vk, uploader_yd, uploader_gd
import configparser


def main():
    def print_counter(iteration): # создаем прогресс бар
        bar = progressbar.ProgressBar()
        for i in bar(range(iteration)):
            time.sleep(0.001)
        bar.finish()

    def get_tokens():
        config = configparser.ConfigParser()
        config.read("settings.ini")  # читаем конфиг
        vk_token = config["TOKENS"]["vk_token"]
        token_ya = config["TOKENS"]["token_ya"]
        return vk_token, token_ya


    vk_token, token_ya = get_tokens()
    vk_id = downloader_vk.Downloader_VK.get_id(screen_name, vk_token) # проверка введён ли id или screen_name
    result = downloader_vk.Downloader_VK(vk_token, vk_id)
    all_photos = result.get_photos(count) # формирование списка с URL 

    uploader = uploader_yd.Uploader_YD(token_ya, folder_name) # загрузка на Yandex Disk
    uploader.folder_creation()
    counter = 1
    for name, link in all_photos.items():
        uploader.upload(name, link)
        print(f'Загружено {counter} фото на YandexDisk, {name} в пaпкe {folder_name}')
        print_counter(counter + 1)
        counter += 1

    def download_to_PC():
        return result.download_on_pc(count)  # локальная загрузка (опционально)
    def upload_to_GD():
        uploadGD = uploader_gd.Uploader_GD() # загрузка фотографий из локальной папки в Google.Drive (опционально)
        folderid = uploadGD.folder_creation(folder_name)
        res = uploadGD.upload(folderid)

    # download = download_to_PC()
    # upload = upload_to_GD()


if __name__ == '__main__':   
    screen_name = 'durov' # (input()) - запрашивать у пользователя id или screen_name
    count = 3 # int(input()) - запрашивать у пользователя количество фотографий
    folder_name = 'Photos from VK' # (input()) запрашивать имя папки
    main()
