from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:Bharat123@localhost/college"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)



class Teacher(db.Model):
    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    department = db.Column(db.String(100))
    salary = db.Column(db.Integer)



@app.route("/teacher", methods=["GET"])
def get_teacher():

    teachers = Teacher.query.all()

    return jsonify([
        {
            "id": t.id,
            "name": t.name,
            "email": t.email,
            "subject": t.department,
            "salary": t.salary
        }
        for t in teachers
    ])


@app.route("/teacher", methods=["POST"])
def save_teacher():

    teacher = Teacher(
        name="Rahul",
        email="rahul@gmail.com",
        subject="mathmatics",
        salary=50000
    )

    db.session.add(teacher)
    db.session.commit()

    return {
        "message": "Employee saved successfully",
        "id": teacher.id
    }


@app.route("/teacher/<int:id>", methods=["PUT"])
def update_teacher(id):

    teacher = db.session.get(Teacher, id)

    if teacher is None:
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


if __name__ == "__main__":

    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
