from src.hh_api import HHApiEmployers, HHApiVacancies
from src.auto_db_creation import auto_create_db
from src.auto_tables_creation import auto_create_tables
from src.employer_validator import Employer
from src.vacancy_validator import Vacancies
from src.db_manager import DBManager


def user_interaction():

    # создаем БД
    auto_create_db()
    # создаем таблицы
    auto_create_tables()

    # вызываем менеджер работы с БД
    db_manager = DBManager()

    # Вызываем классы подключения к API HH для получения данных работодателей
    hh_employers = HHApiEmployers()

    # Загружаем список работодателей в формате JSON
    employers_data = hh_employers.load_employers()

    # инициализируем пустой список для записи экземпляров класса Employer
    employers_examples = []

    # обрезаем лишние данные через класс
    for employer in employers_data:
        emp = Employer.from_dict(employer)
        employers_examples.append(emp)

    # инициализируем пустой список для записи данных о работодателях в формате JSON
    employers_dicts = []

    # возвращаем экземпляры обратно в формат JSON
    for employer in employers_examples:
        employers_dicts.append(employer.to_dict())

    # Грузим работодателей в таблицу employers в БД
    db_manager.insert_employers(employers_dicts)

    # все то же самое для вакансий
    hh_vacancies = HHApiVacancies()

    vacancies = hh_vacancies.load_vacancies()

    vacancies_examples = []

    for vacancy in vacancies:
        vac = Vacancies.from_dict(vacancy)
        vacancies_examples.append(vac)

    vacancies_dicts = []

    for vacancy in vacancies_examples:
        vacancies_dicts.append(vacancy.to_dict())

    db_manager.insert_vacancies(vacancies_dicts)

    user_input = None

    while user_input != "6":
        user_input = input("""
        Введите значение, которое соответствует необходимому действию:
        1 - получить список всех компаний и количество вакансий у каждой компании
        2 - получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        3 - получить среднюю зарплату по вакансиям
        4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
        5 - получить список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        6 - закрыть соединение с БД
        """)
        if user_input == '1':
            result = db_manager.get_companies_and_vacancies_count()
            for i in result:
                print(i, end='\n')
        elif user_input == '2':
            result = db_manager.get_all_vacancies()
            for i in result:
                print(i, end='\n')
        elif user_input == '3':
            result = db_manager.get_avg_salary()
            print(f'Средняя зарплата: {result}')
        elif user_input == '4':
            result = db_manager.get_vacancies_with_higher_salary()
            for i in result:
                print(i, end='\n')
        elif user_input == '5':
            keyword_input = input('''
            Введите ключевое слово для поиска
            ''')
            result = db_manager.get_vacancies_with_keyword(keyword_input)
            for i in result:
                print(i, end='\n')
        else:
            print('Соедниние с БД закрыто, спасибо')
            db_manager.close_connection()
            break


user_interaction()
