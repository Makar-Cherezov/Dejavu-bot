import psycopg2
from psycopg2 import sql
import os


# Функция для подключения к базе данных
def connect_to_db():
    try:
        # Подключение к PostgreSQL
        connection = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB', 'postgres'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', '123'),
            # host=os.getenv('DB_HOST', 'postgres'),  # Имя сервиса из docker-compose.yml
            host=os.getenv('DB_HOST', '87.242.118.224'),
            port=os.getenv('DB_PORT', '5432')
        )
        print("Успешное подключение к базе данных")
        return connection
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        raise


# Функция для выборки данных из таблицы example
def select_from_example_table(connection):
    try:
        cursor = connection.cursor()

        # Выполняем запрос
        query = sql.SQL("SELECT * FROM example;")
        cursor.execute(query)

        # Получаем все строки
        rows = cursor.fetchall()

        if not rows:
            print("Таблица пуста")
        else:
            print("Данные из таблицы example:")
            for row in rows:
                print(row)

        cursor.close()
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        raise
    finally:
        if connection:
            connection.close()
            print("Соединение с базой данных закрыто")


if __name__ == "__main__":
    # Подключаемся к базе данных
    connection = connect_to_db()

    if connection:
        # Выбираем данные из таблицы example
        select_from_example_table(connection)