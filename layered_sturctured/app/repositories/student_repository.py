from extensions import db
from app.models.student import Student


def get_all():
    return Student.query.all()


def get_by_id(student_id):
    return Student.query.get(student_id)


def create(student):
    db.session.add(student)
    db.session.commit()

    return student


def update(student):
    db.session.commit()

    return student


def delete(student):
    db.session.delete(student)
    db.session.commit()