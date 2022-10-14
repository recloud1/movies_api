import json
from json import JSONDecodeError


class JsonReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> dict:
        """Чтение файла настроек индекса для Elasticsearch"""
        with open(self.file_path, 'r') as file:
            try:
                data: dict = json.load(file)
            except JSONDecodeError:
                raise ValueError('Файл настроек индекса для Elastic Search не заполнен')

        if not data.get('settings'):
            raise ValueError('Секция settings для индекса отсутствует')

        if not data.get('mappings'):
            raise ValueError('Секция mapping для индекса отсутствует')

        return data
