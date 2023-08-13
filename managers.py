
import sqlite3
from typing import Optional

from settings import DATABASE_SETTINGS


class BaseManager:

    database_settings = DATABASE_SETTINGS
    connection = None

    def __init__(self, model_class):
        self.model_class = model_class

    def __del__(self):
        # Закрываем соединение с базой данных, если оно существует
        self._close_database_connection()

    @classmethod
    def _set_database_connection(cls) -> None:
        """Устанавливает в поле connection соединение с базой данных sqlite3,
        указанной в модуле settings в поле DATABASE_SETTINGS"""
        cls.connection = sqlite3.connect(cls.database_settings.get('database'))

    @classmethod
    def _close_database_connection(cls) -> None:
        """Закрывает соединение с базой данных sqlite3"""
        if cls.connection is not None:
            cls.connection.close()
        cls.connection = None

    @classmethod
    def _get_cursor(cls) -> sqlite3.Cursor:
        """Возвращает курсор для базы данных"""
        if cls.connection is None:
            cls._set_database_connection()
        return cls.connection.cursor()

    @classmethod
    def _execute_query(cls, query: str):
        """Выполняет запрос query к базе данных"""
        cursor = cls._get_cursor()
        cursor.execute(query)
        cls.connection.commit()
        cursor.close()

    def select(self, *, field_names: list | tuple, piece_size: int = 200) -> Optional[list]:
        """Возвращает значения из полей field_names базы данных"""

        query = f"SELECT {', '.join(field_names)} FROM {self.model_class.table_name}"

        cursor = self._get_cursor()
        cursor.execute(query)

        model_objects = []

        is_fetching_completed = False
        while not is_fetching_completed:
            result = cursor.fetchmany(piece_size)
            if len(result) == 0:
                print('[INFO] Значения в базе данных отсутствуют')
                return []
            for row in result:
                keys, values = field_names, row
                row_data = dict(zip(keys, values))
                model_objects.append(self.model_class(**row_data))
            is_fetching_completed = len(result) < piece_size

        cursor.close()

        print('[INFO] Выборка значений из базы данных успешно выполнена')

        return model_objects

    def insert(self, lines: list | tuple):
        """Вставляет новые значения в базу данных"""
        field_names = lines[0].keys()

        assert all(line.keys() == field_names for line in lines[1:]), \
            "[ERROR] Не все ряды имеют одинаковые поля при вставке значений"

        fields_format = ", ".join(field_names)

        for line in lines:
            values_format = [f'"{value}"' for value in map(str, line.values())]
            query = f"INSERT INTO {self.model_class.table_name} ({fields_format}) " \
                    f"VALUES ({', '.join(values_format)})"

            self._execute_query(query)

        print('[INFO] Вставка значений в базу данных успешно выполнена')

    def update(self, column, delta):
        """Изменяет существующий целочисленный столбец column в таблице на значение delta"""

        query = f"UPDATE {self.model_class.table_name} "\
                f"SET {column} = {column} + {delta};"

        self._execute_query(query)

        print('[INFO] Изменение существующего столбца в базе данных выполнено')

    def delete(self):
        """Удаляет все значения в базе данных"""
        query = f"DELETE FROM {self.model_class.table_name};"

        self._execute_query(query)

        print('[INFO] Удаление значений в базе данных успешно выполнено')
