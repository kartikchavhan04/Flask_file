from flask import Blueprint, request, jsonify

from app.services import employee_service


employee_bp = Blueprint(
    "employee",
    __name__
)


@employee_bp.route(
    "/employees",
    methods=["POST"]
)
def create_employee():

    data = request.get_json()

    employee, error = employee_service.create_employee(data)

    if error:
        return jsonify({
            "message": error
        }), 400

    return jsonify({
        "message": "Employee created successfully",
        "employee": {
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "salary": employee.salary
        }
    }), 201


@employee_bp.route(
    "/employees",
    methods=["GET"]
)
def get_employees():

    employees = employee_service.get_employees()

    result = []

    for employee in employees:

        result.append({
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "salary": employee.salary
        })

    return jsonify(result), 200


@employee_bp.route(
    "/employees/<int:id>",
    methods=["GET"]
)
def get_employee(id):

    employee = employee_service.get_employee(id)

    if employee is None:
        return jsonify({
            "message": "Employee not found"
        }), 404

    return jsonify({
        "id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "salary": employee.salary
    }), 200


@employee_bp.route(
    "/employees/<int:id>",
    methods=["PUT"]
)
def update_employee(id):

    data = request.get_json()

    employee = employee_service.update_employee(
        id,
        data
    )

    if employee is None:
        return jsonify({
            "message": "Employee not found"
        }), 404

    return jsonify({
        "message": "Employee updated successfully"
    }), 200


@employee_bp.route(
    "/employees/<int:id>",
    methods=["DELETE"]
)
def delete_employee(id):

    employee = employee_service.delete_employee(id)

    if employee is None:
        return jsonify({
            "message": "Employee not found"
        }), 404

    return jsonify({
        "message": "Employee deleted successfully"
    }), 200