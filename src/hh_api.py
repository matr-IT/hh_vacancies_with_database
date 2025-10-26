from abc import ABC

import requests


class HHApiAbstract(ABC):
    """
    Абстрактный класс для получения вакансий
    """

    pass


class HHApiEmployers(HHApiAbstract):
    """
    Класс для работы с API HeadHunter - получение данных работодателей по их id
    """

    def __init__(self):
        self.__url = f"https://api.hh.ru/employers/"  # employers/{employer_id}
        self.__headers = {"User-Agent": "HHApi-User-Agent"}
        self.__employers = []
        self.__employers_ids = [
            1740,
            15478,
            39305,
            87021,
            2180,
            907345,
            853364,
            2324020,
            127256,
            1057,
        ]
        super().__init__()

    def load_employers(self):
        """
        Получение работодателей через API HH по id
        """

        for i in self.__employers_ids:
            response = requests.get(self.__url + str(i), headers=self.__headers)
            if response.status_code == 200:
                employer = response.json()
                self.__employers.append(employer)
            else:
                return "Возникла ошибка запроса"
        return self.__employers


class HHApiVacancies(HHApiAbstract):
    """
    Класс для работы с API HeadHunter - получение списков вакансий по id работодателей
    """

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"employer_id": ""}
        self.__vacancies = []
        self.__employers_ids = [
            1740,
            15478,
            39305,
            87021,
            2180,
            907345,
            853364,
            2324020,
            127256,
            1057,
        ]
        super().__init__()

    def load_vacancies(self):
        """
        Получение вакансий через API HH по id компаний-работодателей
        """
        for i in self.__employers_ids:
            self.__params["employer_id"] = str(i)
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            if response.status_code == 200:
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
            else:
                return "Возникла ошибка запроса"
        return (self.__vacancies)



