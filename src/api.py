import requests
import os
from src.constants import TOKEN
from abc import ABC, abstractmethod


class BaseApi(ABC):
    """
    Базовый класс для классов API
    """
    @abstractmethod
    def __init__(self):
        """
        Параметры self.url: str
        self.headers: dict подлежат обязательному
        определению в потомках.
        """

    def get_vacancies(self, params_to_search: dict = None) -> str:
        """
        Делает get запрос, бросает исключение если код ответа не 200
        :param params_to_search:
            Параметры запроса для поиска вакансий
        :return:
            Строка данных из ответа api если код ответа 200
        """
        r = requests.get(self.url, headers=self.headers, params=params_to_search)
        if r.status_code == requests.codes.ok:
            data = r.content.decode()
            r.close()
            return data
        r.raise_for_status()


class SJApi(BaseApi):
    """Класс получения вакансий средствами api SuperJob"""
    def __init__(self, api_key=os.getenv(TOKEN)):
        """
        Адрес api, заголовки и токен для запросов вакансий с SuperJob
        бросает исключение если токена нет
        """

        if not api_key:
            raise Exception('SuperJob token not found')

        self.headers = {
            'Host': 'api.superjob.ru',
            'X-Api-App-Id': api_key,
            'Authorization': 'Bearer r.000000010000001.example.access_token',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        self.url = 'https://api.superjob.ru/2.0/vacancies/'


class HHApi(BaseApi):
    """Класс получения вакансий средствами api hh.ru"""
    def __init__(self):
        """Адрес api и заголовки для запросов вакансий с hh"""

        self.headers = {
            'User-Agent': 'api-test-agent'
        }

        self.url = 'https://api.hh.ru/vacancies'
