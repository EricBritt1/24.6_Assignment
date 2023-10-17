import email_validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from models import User

def unique_username(form, field):
    user = User.query.get(field.data)
    if (user):
        raise ValidationError(f'Username Taken!')

def unique_email(form, field):
    email = User.query.get(field.data)
    if (email):
        raise ValidationError(f'Account with email already exists!')



class RegisterUserForm(FlaskForm):

    username = StringField("Create Username", validators=[InputRequired(message="Username required"), Length(max=30, message="May not exceed 30 characters"), unique_username])

    password = PasswordField("Create Password", validators=[InputRequired(message="Password required")])

    email = StringField("Enter Email", validators=[InputRequired(message="Email required"), Email(), Length(max=50, message="Email address must be less than 50 characters long"), unique_email])

    first_name = StringField("First Name", validators=[InputRequired(message="First name required"), Length(max=30, message="May not exceed 30 characters")])

    last_name = StringField("Last Name", validators=[InputRequired(message="Last name required"), Length(max=30, message="May not exceed 30 characters")])

class LogInForm(FlaskForm):

    username = StringField("Enter Username", validators=[InputRequired(message="Username required")])

    password = PasswordField("Enter Password", validators=[InputRequired(message="Password required")])

class FeedbackForm(FlaskForm):
    title = StringField("Enter Title:", validators=[InputRequired(message="Title required!"), Length(max=100, message="May not exceed 30 characters")])
    content = StringField("Enter Content:", validators=[InputRequired(message="Content required!")])

class UpdateFeedbackForm(FlaskForm):
    title = StringField("Update Title:", validators=[InputRequired(message="Title required!"), Length(max=100, message="May not exceed 30 characters")])
    content = StringField("Update Content:", validators=[InputRequired(message="Content required!")])