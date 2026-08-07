from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    DateField,
    SelectField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import DataRequired, Email, Length


class StudentForm(FlaskForm):

    roll_no = StringField(
        "Roll Number",
        validators=[DataRequired()]
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
        validators=[DataRequired()]
    )

    gender = SelectField(
        "Gender",
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ]
    )

    dob = DateField(
        "Date of Birth",
        validators=[DataRequired()]
    )

    address = TextAreaField(
        "Address",
        validators=[DataRequired()]
    )

    submit = SubmitField("Add Student")