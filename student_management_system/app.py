from flask import Flask , render_template,redirect,flash,url_for
from flask import session
from functools import wraps
from extensions import db
from config import Config
from forms import StudentForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,LoginManager,login_user,current_user,logout_user

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

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
        hashed_password = generate_password_hash(form.password.data)

        student = Student(
            roll_no=form.roll_no.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            gender=form.gender.data,
            password=hashed_password

        )
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()

        flash("Student Added Successfully!", "success")

        return redirect(url_for("login"))

    return render_template("add_student.html", form=form)

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

    # फक्त स्वतःचा student edit करू शकतो
    if id != session["student_id"]:
        flash("You can edit only your own information.", "danger")
        return redirect(url_for("students"))

    student = Student.query.get_or_404(id)

    form = StudentForm(obj=student)

    if form.validate_on_submit():

        student.roll_no = form.roll_no.data
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.email = form.email.data
        student.phone = form.phone.data
        student.gender = form.gender.data

        db.session.commit()

        flash("Your information updated successfully.", "success")

        return redirect(url_for("students"))

    return render_template(
        "edit.html",
        form=form
    )
@app.route("/delete-student/<int:id>")
@login_required
def delete_student(id):

    # फक्त स्वतःचा student delete करू शकतो
    if id != session["student_id"]:
        flash("You can delete only your own information.", "danger")
        return redirect(url_for("students"))

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    # Logout because current student account is deleted
    session.pop("student_id", None)

    flash("Your account has been deleted successfully.", "success")

    return redirect(url_for("login"))


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

    student_id = session.get("student_id")

    student = Student.query.get_or_404(student_id)

    return render_template(
        "profile.html",
        student=student
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