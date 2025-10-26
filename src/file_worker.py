import json
import os
from abc import ABC, abstractmethod


class FileWorkerEmployers(ABC):
    """
    Абстрактный класс для работы с файлами
    """

    @abstractmethod
    def add_employer(self, vacancy):
        pass

    @abstractmethod
    def get_employer(self):
        pass


class JsonFileWorkerEmployer(FileWorkerEmployers):
    """
    Класс для работы с JSON-файлами
    """

    def __init__(self, file="employers.json"):
        self.__file = file

        if not os.path.exists(self.__file):
            with open(self.__file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def add_employer(self, employer):
        """
        Метод добавления вакансии в файл
        """
        with open(self.__file, "r", encoding="utf-8") as f:
            employers = json.load(f)
        if employer not in employers:
            employers.append(employer)
        with open(self.__file, "w", encoding="utf-8") as f:
            json.dump(employers, f, indent=4, ensure_ascii=False)

    def get_employer(self):
        """
        Метод получения вакансий из файла
        """
        with open(self.__file, "r", encoding="utf-8") as f:
            employers = json.load(f)
        return employers


class FileWorkerVacancy(ABC):
    """
    Абстрактный класс для работы с файлами
    """

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancy(self):
        pass



class JsonFileWorkerVacancy(FileWorkerVacancy):
    """
    Класс для работы с JSON-файлами
    """

    def __init__(self, file="vacancies.json"):
        self.__file = file

        if not os.path.exists(self.__file):
            with open(self.__file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def add_vacancy(self, vacancy):
        """
        Метод добавления вакансии в файл
        """
        with open(self.__file, "r", encoding="utf-8") as f:
            vacancies = json.load(f)
        if vacancy not in vacancies:
            vacancies.append(vacancy)
        with open(self.__file, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, indent=4, ensure_ascii=False)

    def get_vacancies(self):
        """
        Метод получения вакансий из файла
        """
        with open(self.__file, "r", encoding="utf-8") as f:
            vacancies = json.load(f)
        return vacancies