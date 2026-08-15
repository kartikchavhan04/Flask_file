from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from app import db
from app.models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    return render_template("home.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        # Check required fields

        if not all([
            full_name,
            email,
            password,
            confirm_password
        ]):

            flash(
                "All fields are required.",
                "error"
            )

            return redirect(
                url_for("auth.register")
            )

        # Check password match

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for("auth.register")
            )

        # Check password length

        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "error"
            )

            return redirect(
                url_for("auth.register")
            )

        # Check email

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Email is already registered.",
                "error"
            )

            return redirect(
                url_for("auth.register")
            )

        # Create user

        user = User(
            full_name=full_name,
            email=email
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html"
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        # Find user by email

        user = User.query.filter_by(
            email=email
        ).first()

        # Check password

        if user and user.check_password(password):

            session["user_id"] = user.id

            session["full_name"] = user.full_name

            session["email"] = user.email

            return redirect(
                url_for("tasks.task_list")
            )

        flash(
            "Invalid email or password.",
            "error"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "login.html"
    )


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("auth.login")
    )