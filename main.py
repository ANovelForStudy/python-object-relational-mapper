
from models import BaseModel


class Employee(BaseModel):
    table_name = "employees"


if __name__ == "__main__":
    employees = Employee.objects.select(
        field_names=['name', 'age'], piece_size=3_000)
    for employee in employees:
        print('Name: {!r:>12} | Age: {:=4}'.format(
            employee.name, employee.age))

    new_data = [
        {"name": "Naomi", "age": 19},
        {"name": "Tanaka", "age": 47},
        {"name": "Kaguya", "age": 17},
    ]

    Employee.objects.insert(lines=new_data)

    employees = Employee.objects.select(
        field_names=['name', 'age'], piece_size=3_000)
    for employee in employees:
        print('Name: {!r:>12} | Age: {:=4}'.format(
            employee.name, employee.age))

    Employee.objects.delete()
