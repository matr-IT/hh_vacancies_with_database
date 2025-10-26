import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def auto_create_tables():
    conn=None
    try:
        # Создаем соединение с основной БД 'postgres'
        conn = psycopg2.connect(
            dbname=os.getenv('db_hh'),
            user=os.getenv('user_hh'),
            password=os.getenv('password_hh'),
            host=os.getenv('host_hh'),
            port=os.getenv('port_hh'),
        )
        cur=conn.cursor()
        cur.execute("""CREATE TABLE employers (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            site_url VARCHAR(255) NOT NULL
            )""")
        conn.commit()
        cur.execute("""CREATE TABLE vacancies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            salary INTEGER,
            short_description TEXT,
            employer_id INTEGER NOT NULL,
            FOREIGN KEY (employer_id) REFERENCES employers (id) ON DELETE CASCADE
            )""")
        conn.commit()
        cur.close()
        print("Таблицы 'employers' и 'vacancies' успешно созданы.")

    except psycopg2.Error as e:
        print(f"Ошибка при создании таблиц: {e}")
    finally:
        if conn:
            conn.close()
