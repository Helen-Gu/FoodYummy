from flask_httpauth import HTTPBasicAuth
from flask import g
from ..models import User
from . import api
from .errors import access_unauthorized, access_forbidden
auth_api = HTTPBasicAuth()

@auth_api.verify_password
def verify_password(email, password):

	user = User.objects(email=email).first()
	if not user:
		return False
	else:
		g.current_user = user
	return user.verify_password(password)

@auth_api.error_handler
def auth_failed():
	return access_unauthorized('Invalid credentials')

@api.before_request
@auth_api.login_required
def before_request():
	if not g.current_user.confirmed:
		return access_forbidden('Unconfirmed user')