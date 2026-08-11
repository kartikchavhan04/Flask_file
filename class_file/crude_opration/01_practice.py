from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
 
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:Bharat123@localhost/college"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
 
db = SQLAlchemy(app)
 
 
class Student(db.Model):
    __tablename__ = "student"
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    marks = db.Column(db.Integer)
 
 
@app.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()
 
    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "marks": s.marks
        }
        for s in students
    ])
 
 
@app.route("/student", methods=["POST"])
def save_student():
 
    student = Student(
        name="Nikhil",
        email="nikhil@gmail.com",
        marks=85
    )
 
    db.session.add(student)
    db.session.commit()
 
    return {
        "message": "Student saved successfully",
        "id": student.id
    }
   
# UPDATE API
@app.route("/student/<int:id>", methods=["PUT"])
def update_student(id):
 
    student = db.session.get(Student, id)
 
    if student is None:
        return jsonify({"message": "Student not found"}), 404
 
    data = request.get_json()
 
    student.name = data.get("name", student.name)
    student.email = data.get("email", student.email)
    student.marks = data.get("marks", student.marks)
 
    db.session.commit()
 
    return jsonify({
        "message": "Student updated successfully",
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "marks": student.marks
    })
 
 
# DELETE API
@app.route("/student/<int:id>", methods=["DELETE"])
def delete_student(id):
 
    student = db.session.get(Student, id)
 
    if student is None:
        return jsonify({"message": "Student not found"}), 404
 
    db.session.delete(student)
    db.session.commit()
 
    return jsonify({
        "message": "Student deleted successfully",
        "id": id
    })
 
 
if __name__ == "__main__":
 
    with app.app_context():
        db.create_all()
 
    print("\n========== REGISTERED ENDPOINTS ==========")
 
    for rule in app.url_map.iter_rules():
        methods = ", ".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
        print(f"{methods:10} {rule}")
 
    print("==========================================\n")
 
    app.run(debug=True)
 