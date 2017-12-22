from flask import jsonify, current_app
from . import api
from .errors import bad_request
from ..models import User

@api.route('/user/<int:id>',methods=['GET'])
def get_user(id):
	user = User.objects(id=int(id)).first()
	if user:
		return jsonify(user.to_json())
	return bad_request("user does not exist")

@api.route('/user/<int:id>/recipe',methods=['GET'])
def get_user_recipe(id):
	user = User.objects(id=id).first()
	if user:
		recipes = jsonify({'user_recipe':[r.to_json() for r in user.recipe]})
	return bad_request("user does not exist")

@api.route('/user/<int:id>/dish',methods=['GET'])
def get_user_dish(id):
	user = User.objects(id=id).first()
	if user:
		recipes = jsonify({'user_dish':[r.to_json() for r in user.recipe]})
	return bad_request("user does not exist")