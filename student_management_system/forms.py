from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    DateField,
    SelectField,
    TextAreaField,
    SubmitField,
)

from wtforms.validators import DataRequired, Email, EqualTo, Length,Regexp
from wtforms import PasswordField


class StudentForm(FlaskForm):

    roll_no = StringField(
        "Roll Number",
        validators=[DataRequired(),Length(max=10)]
    )

    first_name = StringField(
        "First Name",
        validators=[DataRequired(), Length(max=50)]
    )

    last_name = StringField(
        "Last Name",
        validators=[DataRequired(), Length(max=50)]
    )

    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    phone = StringField(
        "Phone",
        validators=[DataRequired(),Length(min=10,max=10)]
    )

    gender = SelectField(
        "Gender",
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ]
    )


    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )


    submit = SubmitField("Add Student")

class LoginForm(FlaskForm):

    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )
    
    submit = SubmitField("Login")

