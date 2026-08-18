from app.models.student import Student
from app.repositories import student_repository


def create_student(data):

    student = Student(
        name=data["name"],
        email=data["email"],
        course=data["course"],
        age=data["age"]
    )

    return student_repository.create(student)


def get_students():

    return student_repository.get_all()


def get_student(student_id):

    return student_repository.get_by_id(student_id)


def update_student(student_id, data):

    student = student_repository.get_by_id(student_id)

    if student is None:
        return None

    student.name = data["name"]
    student.email = data["email"]
    student.course = data["course"]
    student.age = data["age"]

    return student_repository.update(student)


def delete_student(student_id):

    student = student_repository.get_by_id(student_id)

    if student is None:
        return None

    student_repository.delete(student)

    return student