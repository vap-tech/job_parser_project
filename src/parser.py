from pydantic import BaseModel, HttpUrl
from typing import Optional
import bleach

from src.vacancy import Vacancy


class SJVacancy(BaseModel):
    """Модель вакансии из ответа SuperJob"""
    id: int  # id Вакансии
    profession: str  # Название вакансии
    date_published: int  # Дата публикации
    compensation: Optional[str] = None  # Условия работы
    candidat: Optional[str] = None  # Требования к кандидату
    town: dict  # Место расположения
    payment_from: Optional[int] = None  # ЗП от
    payment_to: Optional[int] = None  # ЗП до
    link: HttpUrl  # Ссылка на вакансию

    def to_vacancy(self):
        """
        :return: Объект класса Vacancy
        """
        des = bleach.clean(self.candidat,  tags=[], strip=True)
        return Vacancy(self.id, self.profession, self.link, self.town['title'], self.payment_from, des)


class SJBaseModel(BaseModel):
    """Базовая модель данных ответа от SuperJob на запрос вакансий"""
    objects: list[SJVacancy]  # Массив с результатами
    total: int  # Общее количество результатов
    more: bool  # Есть ли ещё результаты

    def get_vacancy(self):
        """
        :return: Список из объектов Vacancy
        """
        return [vac.to_vacancy() for vac in self.objects]


class HHVacancy(BaseModel):
    """Модель данных Вакансия"""
    id: int  # id вакансии
    name: str  # Название
    alternate_url: Optional[HttpUrl] = None  # URL вакансии
    area: dict  # Место расположения
    created_at: str  # Дата и время публикации вакансии
    salary: Optional[dict] = None  # Зарплата
    snippet: Optional[dict] = None  # Фрагмент описания

    def to_vacancy(self):
        """
        :return: Объект класса Vacancy
        """
        # Ищем непустую зарплату
        pay = 0
        if self.salary:
            if self.salary['from']:
                pay = self.salary['from']
            elif self.salary['to']:
                pay = self.salary['to']

        des = "".join([i for i in self.snippet.values() if i])
        des = bleach.clean(des,  tags=[], strip=True)
        url_ = self.alternate_url if self.alternate_url else "Нет Url'а"

        return Vacancy(self.id, self.name, url_, self.area['name'], pay, des)


class HHBaseModel(BaseModel):
    """Базовая модель данных ответа от HH на запрос вакансий"""
    items: list[HHVacancy]  # Список сокращенных представлений резюме
    found: int  # Найдено результатов
    page: int  # Номер страницы
    pages: int  # Всего страниц
    per_page: int  # Результатов на странице
    hidden_on_page: Optional[int] = None  # Количество удаленных или скрытых соискателями резюме на странице

    def get_vacancy(self):
        """
        :return: Список из объектов Vacancy
        """
        return [vac.to_vacancy() for vac in self.items]


class JsonVacancy(BaseModel):
    """Модель данных вакансии из файла json"""
    id: int
    name: str
    url: Optional[HttpUrl] = None
    area: str
    salary: int
    descr: str

    def to_vacancy(self):
        """
        :return: Объект класса Vacancy
        """
        url_ = self.url if self.url else "Нет Url'а"
        return Vacancy(self.id, self.name, url_, self.area, self.salary, self.descr)


class JsonBaseModel(BaseModel):
    """Модель для файла json"""
    items: list[JsonVacancy]

    def get_vacancy(self):
        return [vac.to_vacancy() for vac in self.items]
