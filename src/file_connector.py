import os
from abc import ABC, abstractmethod


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

    def add(self, data):
        with open(self.path, 'w') as f:
            f.write(data)

    def get(self):
        with open(self.path, 'r') as f:
            return f.read()

    def clear(self):
        with open(self.path, 'w') as f:
            f.write('\n')
