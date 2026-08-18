from flask import Blueprint, request, jsonify

from app.services import student_service


student_bp = Blueprint(
    "student",
    __name__
)


@student_bp.route(
    "/students",
    methods=["POST"]
)
def create_student():

    data = request.get_json()

    student = student_service.create_student(data)

    return jsonify({
        "message": "Student created successfully",
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "course": student.course,
            "age": student.age
        }
    }), 201


@student_bp.route(
    "/students",
    methods=["GET"]
)
def get_students():

    students = student_service.get_students()

    result = []

    for student in students:

        result.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "course": student.course,
            "age": student.age
        })

    return jsonify(result), 200


@student_bp.route(
    "/students/<int:id>",
    methods=["GET"]
)
def get_student(id):

    student = student_service.get_student(id)

    if student is None:
        return jsonify({
            "message": "Student not found"
        }), 404

    return jsonify({
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "course": student.course,
        "age": student.age
    }), 200


@student_bp.route(
    "/students/<int:id>",
    methods=["PUT"]
)
def update_student(id):

    data = request.get_json()

    student = student_service.update_student(
        id,
        data
    )

    if student is None:
        return jsonify({
            "message": "Student not found"
        }), 404

    return jsonify({
        "message": "Student updated successfully"
    }), 200


@student_bp.route(
    "/students/<int:id>",
    methods=["DELETE"]
)
def delete_student(id):

    student = student_service.delete_student(id)

    if student is None:
        return jsonify({
            "message": "Student not found"
        }), 404

    return jsonify({
        "message": "Student deleted successfully"
    }), 200