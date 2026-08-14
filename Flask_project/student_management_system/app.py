from flask import Flask , render_template,redirect,flash,url_for,request,session
from functools import wraps
from extensions import db
from config import Config
from forms import StudentForm, LoginForm,EditStudentForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,LoginManager,login_user,current_user,logout_user
import os

from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "student_id" not in session:
            flash("Please login first", "warning")
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated_function



from models import Student

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add-student", methods=["GET", "POST"])
def add_student():

    form = StudentForm()

    if form.validate_on_submit():

        existing_student = Student.query.filter_by(
            email=form.email.data
        ).first()

        if existing_student:

            flash(
                "This email is already registered.",
                "danger"
            )

            return render_template(
                "add_student.html",
                form=form
            )

        hashed_password = generate_password_hash(
            form.password.data
        )

        student = Student(
            roll_no=form.roll_no.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            gender=form.gender.data,
            password=hashed_password
        )

        db.session.add(student)
        db.session.commit()

        flash(
            "Student Added Successfully!",
            "success"
        )

        return redirect(url_for("login"))

    return render_template(
        "add_student.html",
        form=form
    )
@app.route("/students")
@login_required
def students():

    students = Student.query.all()

    return render_template(
        "students.html",
        students=students
    )

@app.route("/edit-student/<int:id>", methods=["GET", "POST"])
@login_required
def edit_student(id):

    student = Student.query.get_or_404(id)

    form = EditStudentForm(obj=student)

    if form.validate_on_submit():

        student.roll_no = form.roll_no.data
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.email = form.email.data
        student.phone = form.phone.data
        student.gender = form.gender.data

        # Password only when user enters a new password
        if form.password.data:

            student.set_password(form.password.data)

        db.session.commit()

        flash("Student Updated Successfully!", "success")

        return redirect(url_for("profile"))

    return render_template(
        "edit.html",
        form=form
    )

@app.route("/delete-student/<int:id>")
@login_required
def delete_student(id):

    # Logged-in student only
    if id != session["student_id"]:
        flash("You can delete only your own account.", "danger")
        return redirect(url_for("profile"))

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    session.pop("student_id", None)

    flash("Your account has been deleted successfully.", "success")

    return redirect(url_for("home"))


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        student = Student.query.filter_by(
            email=form.email.data
        ).first()

        if student and student.check_password(form.password.data):

            session["student_id"] = student.id

            flash("Login Successful", "success")

            return redirect(url_for("profile"))

        else:

            flash("Invalid Email or Password", "danger")

    return render_template(
        "login.html",
        form=form
    )

@app.route("/profile")
@login_required
def profile():

    student = Student.query.get_or_404(
        session["student_id"]
    )

    students_count = Student.query.count()

    return render_template(
        "profile.html",
        student=student,
        students_count=students_count
    )

@app.route("/logout")
def logout():

    session.pop("student_id", None)

    flash("Logout Successfully!", "success")

    return redirect(url_for("login"))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)