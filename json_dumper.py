"""
Модуль для работы с JSON-файлом.

Этот модуль предоставляет класс `DumpJSON`, который позволяет создавать, 
читать и добавлять данные в JSON-файл. Он обрабатывает случаи, когда файл 
не существует или содержит некорректные данные.

Класс `DumpJSON` предлагает следующие функции:
- Создание нового JSON-файла с пустым списком.
- Добавление данных в существующий JSON-файл, в том числе обработка 
  случаев, когда файл не может быть прочитан из-за отсутствия или формата 
  данных.

Основные методы:
- create_json: Создает новый JSON-файл, перезаписывая существующий.
- add_to_json: Добавляет новые данные в существующий JSON-файл, 
  обрабатывая возможные ошибки при загрузке eго содержимого.
"""
import json
from typing import Any

class DumpJSON:
    """Класс для работы с JSON-файлом."""
    def __init__(self) -> None:
        pass

    def create_json(self) -> None:
        """
        Создает новый JSON-файл с пустым списком.
        Если файл уже существует, он будет перезаписан.
        """
        json_data = []
        with open('photos.json', 'w') as file:
            json.dump(json_data, file)

    def add_to_json(self, json_data: Any) -> None:
        """
        Добавляет данные в существующий JSON-файл.
        Если файл не существует или содержит неверные данные, может возникнуть ошибка.

        Args:
            json_data (Any): Данные, которые нужно добавить в JSON-файл.
        """
        try:
            with open("photos.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(json_data)

        with open("photos.json", "w") as file:
            json.dump(data, file)

