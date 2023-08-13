
from models import BaseModel


class Employee(BaseModel):
    table_name = "employees"


def print_elements(employees):
    """Выводит форматированные строки для каждого элемента в контейнере employees"""
    for employee in employees:
        print('Name: {!r:>10} | Age: {:=4}'.format(
            employee.name, employee.age))


if __name__ == "__main__":

    # Проверка операции SELECT
    employees = Employee.objects.select(
        field_names=['name', 'age'], piece_size=3_000)

    print_elements(employees)

    new_data = [
        {"name": "Naomi", "age": 19},
        {"name": "Tanaka", "age": 47},
        {"name": "Kaguya", "age": 17},
    ]

    # Проверка операции INSERT
    Employee.objects.insert(lines=new_data)

    # ПРОВЕРКА ОПЕРАЦИИ UPDATE
    Employee.objects.update(column="age", delta=33)

    employees = Employee.objects.select(
        field_names=['name', 'age'], piece_size=3_000)

    print_elements(employees)

    # Проверка операции DELETE
    Employee.objects.delete()
