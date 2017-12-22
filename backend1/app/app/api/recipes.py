from flask import jsonify, request, g
from . import api
from .errors import bad_request
from ..models import Recipe, Dish

@api.route('/recipe',methods=['GET'])
def get_recipes():
	recipes = Recipe.objects()
	if recipes:
		return jsonify({'all_recipe':[recipe.to_json() for recipe in recipes]})
	return bad_request('no recipe found')

@api.route('/recipe',methods=['POST'])
def post_recipe():
	if request.json is None:
		bad_request("use POST to post recipe data")
	recipe = Recipe.from_json_custom(request.json)
	recipe.author = g.current_user
	recipe.save()
	g.current_user.recipe.append(recipe)
	g.current_user.save()
	return jsonify(recipe.to_json(),201)

@api.route('/recipe/<int:recipe_id>',methods=['GET'])
def get_recipe(recipe_id):
	recipe = Recipe.objects(rid=recipe_id).first()
	if recipe:
		return jsonify(recipe.to_json())
	return bad_request("recipe does not exist")


@api.route('/recipe/<int:recipe_id>/dish',methods=['POST'])
def post_dish(recipe_id):
	parent = Recipe.objects(rid=recipe_id).first()
	if parent is None:
		return bad_request("recipe does not exist")
	if request.json is None:
		return bad_request("use POST to post dish data")
	dish = Dish.from_json(request.json)
	dish.author = g.current_user
	dish.parent = parent
	dish.save()
	g.current_user.dish.append(dish)
	g.current_user.save()
	return jsonify(dish.to_json(),201)

@api.route('/recipe/<int:recipe_id>/dish',methods=['GET'])
def get_dish(recipe_id):
	dishes = Dish.objects(parent__rid=recipe_id)
	if dishes:
		return jsonify({'all_dishes':[d.to_json() for d in dishes]})
	return bad_request("dishes do not exist")	