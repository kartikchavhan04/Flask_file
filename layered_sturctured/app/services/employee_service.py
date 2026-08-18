from app.models.employee import Employee
from app.repositories import employee_repository


def create_employee(data):

    existing_employee = employee_repository.get_by_name(
        data["name"]
    )

    if existing_employee:
        return None, "Employee already exists"

    employee = Employee(
        name=data["name"],
        email=data["email"],
        salary=data["salary"]
    )

    employee = employee_repository.create(employee)

    return employee, None


def get_employees():

    return employee_repository.get_all()


def get_employee(employee_id):

    return employee_repository.get_by_id(employee_id)


def update_employee(employee_id, data):

    employee = employee_repository.get_by_id(employee_id)

    if employee is None:
        return None

    employee.name = data["name"]
    employee.email = data["email"]
    employee.salary = data["salary"]

    return employee_repository.update(employee)


def delete_employee(employee_id):

    employee = employee_repository.get_by_id(employee_id)

    if employee is None:
        return None

    employee_repository.delete(employee)

    return employee