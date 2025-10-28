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
    bd_manager = DBManager()

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
    bd_manager.insert_employers(employers_dicts)

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

    bd_manager.insert_vacancies(vacancies_dicts)


user_interaction()
