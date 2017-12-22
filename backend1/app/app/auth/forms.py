from wtforms import Form, StringField, BooleanField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from . import auth
from wtforms import ValidationError
from ..models import User
import logging

class LoginForm(Form):
    email = StringField(validators=[Required(), Length(1, 64),Email()])
    password = PasswordField(validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


    def get_user(self):
        return User.objects(email=self.email.data).first()

class RegisterForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
Email("valid email address only")])
    username = StringField("Username", validators=[Required(), Length(1,50), Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
'Usernames must have only letters, numbers, or underscores')])
    password = PasswordField("Password",validators=[Required(),EqualTo("confirm", message="Passworld do not match")])

    confirm = PasswordField("Confirm Password")
    submit = SubmitField('Register')


	