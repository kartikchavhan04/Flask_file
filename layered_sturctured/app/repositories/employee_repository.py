from extensions import db
from app.models.employee import Employee


def get_all():
    return Employee.query.all()


def get_by_id(employee_id):
    return Employee.query.get(employee_id)


def get_by_name(name):
    return Employee.query.filter_by(name=name).first()


def create(employee):
    db.session.add(employee)
    db.session.commit()

    return employee


def update(employee):
    db.session.commit()

    return employee


def delete(employee):
    db.session.delete(employee)
    db.session.commit()