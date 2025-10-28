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
            dbname=os.getenv('db_hh'),
            user=os.getenv('user_hh'),
            password=os.getenv('password_hh'),
            host=os.getenv('host_hh'),
            port=os.getenv('port_hh'),
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
                    (employer['id'], employer['name'], employer['site_url'])
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
                required_fields = ['name', 'employer_id', 'url']
                missing_fields = [field for field in required_fields if field not in vacancy or vacancy[field] is None]

                if missing_fields:
                    print(f"Пропуск вакансии без обязательных полей {missing_fields}: {vacancy.get('name', 'Unknown')}")
                    skipped += 1
                    continue

                self.cur.execute(
                    """
                    INSERT INTO vacancies (name, salary, short_description, employer_id, url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        vacancy['name'],
                        vacancy.get('salary'),
                        vacancy.get('short_description', ''),
                        vacancy['employer_id'],
                        vacancy['url']
                    )
                )
                count += 1

            self.conn.commit()
            print(f"Успешно добавлено {count} вакансий, пропущено {skipped} вакансий")
            return count

        except Exception as e:
            self.conn.rollback()
            print(f"Ошибка при добавлении вакансий: {e}")
            raise