from wtforms import Form, StringField, BooleanField, TextAreaField, PasswordField, SubmitField, SelectField
from wtforms.validators import Required, Length, Regexp, EqualTo, Email
from . import main
from ..models import Role, User

class EditProfileForm(Form):
	new_name = StringField(validators=[Required(), Length(1,50), Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
'Usernames must have only letters, numbers, or underscores')])
	password = PasswordField(validators=[Required(),EqualTo("confirm", message="Passworld do not match")])
	confirm = PasswordField("Confirm Password")
	submit = SubmitField('Update')

class EditProfileAdminForm(Form):
	email = StringField('Email', validators=[Length(1, 64),
		Email()])
	username = StringField('Username', validators=[Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
			'Usernames must have only letters, numbers or underscores')])
	password = StringField("Password")
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role', coerce=int)
	submit = SubmitField('Submit')

	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		self.role.choices = [(role.permissions, role.name) for role in Role.objects]
		self.user = user

	def validate_email(self, field):
		if field.data != self.user.email and User.objects(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if User.objects(username=field.data).first():
			raise ValidationError('Username already exists.')	