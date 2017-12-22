from flask import jsonify
from . import api

def bad_request(e):
	response = jsonify(error='bad request',message=e)
	response.status_code = 400
	return response

def access_unauthorized(e):
	response = jsonify(error='unathorized access',message=e)
	response.status_code = 401
	return response

def access_forbidden(e):
	response = jsonify(error='forbidden access',message=e)
	response.status_code = 403
	return response

@api.errorhandler(ValueError)
def validation_failed(e):
	return bad_request(e)