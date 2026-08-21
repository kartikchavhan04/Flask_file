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
    __tablename__ = "teacher"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    subject = db.Column(db.String(100))
    salary = db.Column(db.Integer)



@app.route("/teacher", methods=["GET"])
def get_teacher():

    teachers = Teacher.query.all()

    return jsonify([
        {
            "id": t.id,
            "name": t.name,
            "email": t.email,
            "subject": t.subject,
            "salary": t.salary
        }
        for t in teachers
    ])



    
@app.route("/teacher",methods=["POST"])
def create_teacher():
    data = request.get_json()
    
    if not data:
        return jsonify({"massage": "NO input data Provided"}),400
    
    teacher = Teacher(
        name = data.get('name'),
        email = data.get('email'),
        subject = data.get('subject'),
        salary = data.get('salary')
    )
    
    db.session.add(teacher)
    db.session.commit()
    
    return jsonify({"massage": "Teacher data saved successfully !"})

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
        "message": "Teacher saved successfully",
        "id": teacher.id
    }


@app.route("/teacher/<int:id>", methods=["PUT"])
def update_teacher(id):

    teacher = db.session.get(Teacher, id)

    if teacher is None:
        return jsonify({
            "message": "Teacher not found"
        }), 404

    data = request.get_json()

    teacher.name = data.get("name", teacher.name)
    teacher.email = data.get("email", teacher.email)
    teacher.subject = data.get(
        "subject",
        teacher.subject
    )
    teacher.salary = data.get(
        "salary",
        teacher.salary
    )

    db.session.commit()

    return jsonify({
        "message": "Teacher updated successfully",
        "id": teacher.id,
        "name": teacher.name,
        "email": teacher.email,
        "subject": teacher.subject,
        "salary": teacher.salary
    })


@app.route("/teacher/<int:id>", methods=["DELETE"])
def delete_teacher(id):

    teacher = db.session.get(Teacher, id)

    if teacher is None:
        return jsonify({
            "message": "Teacher not found"
        }), 404

    db.session.delete(teacher)
    db.session.commit()

    return jsonify({
        "message": "Teacher deleted successfully",
        "id": id
    })


if __name__ == "__main__":

    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
