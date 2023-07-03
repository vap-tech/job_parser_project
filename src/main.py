from src.functions import collector, input_source
from src.file_connector import JsonConnector
from src.area_selector import AreaSelector
from src.constants import FILENAME


def main():

    src = input_source()  # Получаем источники вакансий
    count = int(input('Сколько вакансий загрузить из каждого источника? '))  # Запросили кол-во вакансий
    area = AreaSelector().get()  # Получаем город
    key_word = input('Введите ключевое слово для поиска: ')  # Получаем ключевое слово

    vacancies = collector(key_word, area, src, count)  # Получаем вакансии из источников

    print('\nВакансии загружены\nОчистить Json?\n')

    jc = JsonConnector(FILENAME)  # Объект для работы с файлом Json

    while True:
        user_input = int(input('1 - да, 0 - нет '))
        if user_input in [0, 1]:
            if user_input:
                jc.clear()
                print('Json файл очищен')
            break
        print('Неправильный ввод')

    print('Отсортировать полученные вакансии по заработной плате?')

    while True:
        user_input = int(input('1 - да, 0 - нет '))
        if user_input in [0, 1]:
            if user_input:
                vacancies.sort(reverse=True)
                print('Вакансии отсортированы')
            break
        print('Неправильный ввод')

    for i in vacancies:
        print(i)

    jc.add(vacancies)
    print('\nВакансии так же добавлены в файл Json')


if __name__ == '__main__':
    main()
