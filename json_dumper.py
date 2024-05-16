import json


def create_json(): # cоздаем json-файл
    json_data = []
    with open('photos.json', 'w') as file:
        file.write(json.dumps(json_data))

create_json()

def add_to_json(json_data): # наполняем json-файл
    data = json.load(open("photos.json"))
    data.append(json_data)
    with open("photos.json", "w") as file:
        json.dump(data, file)