from abc import ABC

class EmployerAbstract(ABC):
    """
    Абстрактный класс для валидации данных работодателей
    """
    pass

class Employer(EmployerAbstract):
    """
    Класс для валидации данных работодателей
    """
    __slots__ = ('__id', '__name', '__site_url')

    __id: int
    __name: str
    __site_url: str

    def __init__(self, id, name, site_url):
        self.__id = id
        self.__name = name
        self.__site_url = site_url

    @classmethod
    def from_dict(cls, dict_employers):
        """
        Метод преобразования словаря в экземпляр класса
        """
        return cls(
            id=dict_employers.get("id"),
            name=dict_employers.get("name"),
            site_url=dict_employers.get("site_url"),
            )

    def to_dict(self):
        """
        Метод преобразования экземпляра класса в словарь
        """
        return {
            "id": self.__id,
            "name": self.__name,
            "site_url": self.__site_url,
        }

    def __str__(self):
        return self.__id, self.__name