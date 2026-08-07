from flask import Flask , render_template,redirect,flash,url_for
from extensions import db
from config import Config
from forms import StudentForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
from models import Student

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add-student", methods=["GET", "POST"])
def add_student():

    form = StudentForm()

    if form.validate_on_submit():

        student = Student(
            roll_no=form.roll_no.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            gender=form.gender.data,
            dob=form.dob.data,
            address=form.address.data
        )

        db.session.add(student)
        db.session.commit()

        flash("Student Added Successfully!", "success")

        return redirect(url_for("add_student"))

    return render_template("add_student.html", form=form)

@app.route("/students")
def students():

    students = Student.query.all()

    return render_template(
        "students.html",
        students=students
    )

@app.route("/edit-student/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    student = Student.query.get_or_404(id)

    form = StudentForm(obj=student)

    if form.validate_on_submit():

        student.roll_no = form.roll_no.data
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.email = form.email.data
        student.phone = form.phone.data
        student.gender = form.gender.data
        student.dob = form.dob.data
        student.address = form.address.data

        db.session.commit()

        flash("Student Updated Successfully", "success")

        return redirect(url_for("students"))

    return render_template(
        "add_student.html",
        form=form
    )

@app.route("/delete-student/<int:id>")
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)

    db.session.commit()

    flash("Student Deleted Successfully", "success")

    return redirect(url_for("students"))


with app.app_context():
    db.create_all()

import routes


if __name__ == "__main__":
    app.run(debug=True)