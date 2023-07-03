import os
import json
import pydantic_core
from abc import ABC, abstractmethod

from src.parser import JsonBaseModel


class Connector(ABC):
    """Абстрактный класс для коннекторов файлов"""
    @abstractmethod
    def add(self, data):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def clear(self):
        pass


class JsonConnector(Connector):
    """Класс работы с JSON файлами"""
    def __init__(self, file_name):
        self.path = os.path.join('..', 'data', file_name)

    @staticmethod
    def list_vacancy_to_str(vacs: list) -> str:
        """
        Преобразует список объектов класса Vacancy к
        заданной структуре для дальнейшего сохранения в файл Json
        :param vacs: Список объектов класса Vacancy
        :return: Строка с данными для записи в Json
        """
        data = {'items': [vac.all_to_dict for vac in vacs]}
        return json.dumps(data, indent=2, ensure_ascii=False)

    def add(self, data: list):
        """
        Добавляет полученный на вход список объектов класса Vacancy
        к содержимому файла Json
        :param data: Список объектов класса Vacancy
        ВАЖНО:
        # Если в функцию передать list и сделать к нему extend
        # list так же меняется в месте вызова!
        """

        new_ = self.get()
        new_.extend(data)
        data = self.list_vacancy_to_str(new_)
        with open(self.path, 'w') as f:
            f.write(data)

    def get(self) -> list:
        """
        Читает файл Json, и возвращает его содержимое в виде списка
        :return: Список объектов класса Vacancy
        """
        with open(self.path, 'r') as f:
            raw = f.read()
        try:
            model = JsonBaseModel.model_validate_json(raw)
        except pydantic_core.ValidationError:
            vacs = []
        else:
            vacs = model.get_vacancy()
        return vacs

    def clear(self):
        with open(self.path, 'w') as f:
            f.write('')
