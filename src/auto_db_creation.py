import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

load_dotenv()


def auto_create_db():
    conn = None
    try:
        # Создаем соединение с основной БД 'postgres'
        conn = psycopg2.connect(
            dbname=os.getenv('dbname'),
            user=os.getenv('user'),
            password=os.getenv('password'),
            host=os.getenv('host'),
            port=os.getenv('port')
        )

        # Устанавливаем уровень изоляции для этого соединения в autocommit
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur = conn.cursor()

        # Выполняем команду CREATE DATABASE
        cur.execute("CREATE DATABASE hh_employers_vacancies;")

        cur.close()
        print("База данных 'hh_employers_vacancies' успешно создана.")

    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        if conn:
            conn.close()



auto_create_db()
