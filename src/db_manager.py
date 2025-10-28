from abc import ABC
import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()


class DBManagerAbstract(ABC):
    """
    Абстрактный класс менеджера БД
    """

    pass


class DBManager(DBManagerAbstract):
    """
    Класс для работы с БД
    """

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("db_hh"),
            user=os.getenv("user_hh"),
            password=os.getenv("password_hh"),
            host=os.getenv("host_hh"),
            port=os.getenv("port_hh"),
        )
        self.cur = self.conn.cursor()

    def insert_employers(self, employers_data: list[dict]) -> int:
        """
        Наполнение таблицы employers данными из списка словарей
        """
        try:
            count = 0
            for employer in employers_data:
                self.cur.execute(
                    """
                    INSERT INTO employers (id, name, site_url)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        name = EXCLUDED.name,
                        site_url = EXCLUDED.site_url
                    """,
                    (employer["id"], employer["name"], employer["site_url"]),
                )
                count += 1

            self.conn.commit()
            print(f"Успешно добавлено/обновлено {count} работодателей")
            return count

        except Exception as e:
            self.conn.rollback()
            print(f"Ошибка при добавлении работодателей: {e}")
            raise

    def insert_vacancies(self, vacancies_data: list[dict]) -> int:
        """
        Наполнение таблицы vacancies данными из списка словарей
        """
        try:
            count = 0
            skipped = 0

            for vacancy in vacancies_data:
                # Проверяем наличие обязательных полей
                required_fields = ["name", "employer_id", "url"]
                missing_fields = [
                    field
                    for field in required_fields
                    if field not in vacancy or vacancy[field] is None
                ]

                if missing_fields:
                    print(
                        f"Пропуск вакансии без обязательных полей {missing_fields}: {vacancy.get('name', 'Unknown')}"
                    )
                    skipped += 1
                    continue

                self.cur.execute(
                    """
                    INSERT INTO vacancies (name, salary, short_description, employer_id, url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        vacancy["name"],
                        vacancy.get("salary"),
                        vacancy.get("short_description", ""),
                        vacancy["employer_id"],
                        vacancy["url"],
                    ),
                )
                count += 1

            self.conn.commit()
            print(f"Успешно добавлено {count} вакансий, пропущено {skipped} вакансий")
            return count

        except Exception as e:
            self.conn.rollback()
            print(f"Ошибка при добавлении вакансий: {e}")
            raise

    def get_companies_and_vacancies_count(self) -> list[dict]:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        try:
            self.cur.execute(
                """
                SELECT e.name, COUNT(v.id) as vacancies_count
                FROM employers e
                LEFT JOIN vacancies v ON e.id = v.employer_id
                GROUP BY e.id, e.name
                ORDER BY vacancies_count DESC
            """
            )

            result = []
            for row in self.cur.fetchall():
                result.append({"company_name": row[0], "vacancies_count": row[1]})

            return result

        except Exception as e:
            print(f"Ошибка при получении списка компаний: {e}")
            return []

    def get_all_vacancies(self) -> list[dict]:
        """
        получаем список всех вакансий
        """
        try:
            self.cur.execute(
                """
                SELECT e.name as company_name, v.name as vacancy_name, 
                       v.salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
                ORDER BY e.name, v.salary DESC NULLS LAST
            """
            )

            result = []
            for row in self.cur.fetchall():
                result.append(
                    {
                        "company_name": row[0],
                        "vacancy_name": row[1],
                        "salary": row[2],
                        "url": row[3],
                    }
                )

            return result

        except Exception as e:
            print(f"Ошибка при получении списка вакансий: {e}")
            return []

    def get_avg_salary(self) -> float:
        """
        получаем среднюю зп по вакансиям
        """
        try:
            self.cur.execute(
                """
                SELECT AVG(salary) as avg_salary
                FROM vacancies
                WHERE salary IS NOT NULL AND salary > 0
            """
            )

            result = self.cur.fetchone()
            return round(float(result[0]), 2) if result and result[0] else 0.0

        except Exception as e:
            print(f"Ошибка при расчете средней зарплаты: {e}")
            return 0.0

    def get_vacancies_with_higher_salary(self) -> list[dict]:
        """
        получаем вакансии с зп выше средней
        """
        try:
            avg_salary = self.get_avg_salary()

            self.cur.execute(
                """
                SELECT e.name as company_name, v.name as vacancy_name, 
                       v.salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
                WHERE v.salary > %s
                ORDER BY v.salary DESC
            """,
                (avg_salary,),
            )

            result = []
            for row in self.cur.fetchall():
                result.append(
                    {
                        "company_name": row[0],
                        "vacancy_name": row[1],
                        "salary": row[2],
                        "url": row[3],
                    }
                )

            return result

        except Exception as e:
            print(f"Ошибка при получении вакансий с высокой зарплатой: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword: str) -> list[dict]:
        """
        Получаем вакансии по ключевому слову
        """
        try:
            search_pattern = f"%{keyword}%"

            self.cur.execute(
                """
                SELECT e.name as company_name, v.name as vacancy_name, 
                       v.salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
                WHERE v.name ILIKE %s
                ORDER BY e.name, v.salary DESC NULLS LAST
            """,
                (search_pattern,),
            )

            result = []
            for row in self.cur.fetchall():
                result.append(
                    {
                        "company_name": row[0],
                        "vacancy_name": row[1],
                        "salary": row[2],
                        "url": row[3],
                    }
                )

            return result

        except Exception as e:
            print(f"Ошибка при поиске вакансий по ключевому слову: {e}")
            return []

    def close_connection(self):
        """Закрывает БД"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Соединение с базой данных закрыто")
