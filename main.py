
import sqlite3
from typing import Optional

from settings import DATABASE_SETTINGS


class BaseManager:

    database_settings = DATABASE_SETTINGS

    def __init__(self, model_class):
        self.model_class = model_class

    def select(self, *, field_names: list | tuple, piece_size: int = 200) -> Optional[list]:

        # Собираем запрос
        fields_format = ', '.join(field_names)
        query = f"SELECT {fields_format} FROM {self.model_class.table_name}"

        connection = sqlite3.connect(self.database_settings.get('database'))
        cursor = connection.cursor()
        cursor.execute(query)

        # Результирующий список объектов
        model_objects = []

        # Проверка на то, извлечены ли все записи из таблицы
        is_fetching_completed = False
        while not is_fetching_completed:
            result = cursor.fetchmany(piece_size)
            for row in result:
                keys, values = field_names, row
                row_data = dict(zip(keys, values))
                model_objects.append(self.model_class(**row_data))
            is_fetching_completed = len(result) < piece_size

        return model_objects

    def insert(self, rows):
        pass

    def update(self, new_data):
        pass

    def delete(self):
        pass


class MetaModel(type):
    manager_class = BaseManager

    def _get_manager_instance(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager_instance()


class BaseModel(metaclass=MetaModel):
    table_name = ""

    def __init__(self, **row_data):
        for field_name, value in row_data.items():
            setattr(self, field_name, value)

    def __repr__(self):
        attrs_format = ", ".join([f'{field}={value}' for field, value in self.__dict__.items()])
        return f"<{self.__class__.__name__}: ({attrs_format})>"


class Employee(BaseModel):
    manager_class = BaseManager
    table_name = "employees"


if __name__ == "__main__":
    print(Employee.objects.model_class)
    employees = Employee.objects.select(field_names=['name', 'age'], piece_size=3_000)
    for employee in employees:
        print(f'Name: {employee.name} | Age: {employee.age}')
