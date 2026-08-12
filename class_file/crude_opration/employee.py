from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQL Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:Bharat123@localhost/college"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)


# =========================
# EMPLOYEE MODEL
# =========================

class Employee(db.Model):
    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    department = db.Column(db.String(100))
    salary = db.Column(db.Integer)


# =========================
# GET ALL EMPLOYEES
# =========================

@app.route("/employees", methods=["GET"])
def get_employees():

    employees = Employee.query.all()

    return jsonify([
        {
            "id": e.id,
            "name": e.name,
            "email": e.email,
            "department": e.department,
            "salary": e.salary
        }
        for e in employees
    ])


# =========================
# CREATE EMPLOYEE
# =========================

@app.route("/employee", methods=["POST"])
def save_employee():

    employee = Employee(
        name="Rahul",
        email="rahul@gmail.com",
        department="IT",
        salary=50000
    )

    db.session.add(employee)
    db.session.commit()

    return {
        "message": "Employee saved successfully",
        "id": employee.id
    }


# =========================
# UPDATE EMPLOYEE
# =========================

@app.route("/employee/<int:id>", methods=["PUT"])
def update_employee(id):

    employee = db.session.get(Employee, id)

    if employee is None:
        return jsonify({
            "message": "Employee not found"
        }), 404

    data = request.get_json()

    employee.name = data.get("name", employee.name)
    employee.email = data.get("email", employee.email)
    employee.department = data.get(
        "department",
        employee.department
    )
    employee.salary = data.get(
        "salary",
        employee.salary
    )

    db.session.commit()

    return jsonify({
        "message": "Employee updated successfully",
        "id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "department": employee.department,
        "salary": employee.salary
    })


# =========================
# DELETE EMPLOYEE
# =========================

@app.route("/employee/<int:id>", methods=["DELETE"])
def delete_employee(id):

    employee = db.session.get(Employee, id)

    if employee is None:
        return jsonify({
            "message": "Employee not found"
        }), 404

    db.session.delete(employee)
    db.session.commit()

    return jsonify({
        "message": "Employee deleted successfully",
        "id": id
    })


# =========================
# CREATE DATABASE TABLE
# =========================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    print("\n========== REGISTERED ENDPOINTS ==========")

    for rule in app.url_map.iter_rules():

        methods = ", ".join(
            sorted(rule.methods - {"HEAD", "OPTIONS"})
        )

        print(f"{methods:10} {rule}")

    print("==========================================\n")

    app.run(debug=True)
