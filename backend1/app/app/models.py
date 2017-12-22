from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import login_manager
from app import db
from flask import current_app, url_for
import datetime


class Permission:
	ADMIN = 16
	MOD_COMMENT = 8
	WRITE_RECIPES = 4
	COMMENT = 2
	FOLLOW = 1

class Role(db.Document):
	name = db.StringField(max_length=50,unique=True)
	default = db.BooleanField(default=False,index=True)
	permissions = db.IntField(default=0)

	@staticmethod
	def insert_roles():
		roles = {
			'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE_RECIPES],
			'Admin': [Permission.FOLLOW, Permission.COMMENT, 
			Permission.WRITE_RECIPES,Permission.MOD_COMMENT, Permission.ADMIN],
		}
		for r in roles:
			role = Role.objects(name=r).first()
			if role is None:
				role = Role(name=r)
				role.set_permission(roles.get(r))
				role.default = (role.name == 'User')
				role.save()

	def set_permission(self, perms):
		for p in perms:
			self.permissions += p

	def remove_permission(self, perms):
		for p in perms:
			self.permission -= p

	def is_permitted(self, p):
		return (self.permissions & p == p)

class User(db.Document): 
	id = db.SequenceField(primary_key=True)
	email = db.StringField(required=True,unique=True,index=True)
	username = db.StringField(max_length=50,required=True,index=True)
	p_hash = db.StringField(max_length=128,required=True)
	confirmed = db.BooleanField(default=False)
	role = db.ReferenceField(Role)
	last_seen = db.DateTimeField(default=datetime.datetime.now)
	avatar = db.StringField(default=None)
	
	recipe = db.ListField(ReferenceField('Recipe'))
	dish = db.ListField(ReferenceField('Dish'))

	def __init__(self,**kwargs):
		super(User, self).__init__(**kwargs)
		if self.role is None:
			if self.email == current_app.config['FY_ADMIN']:
				self.role = Role.objects(name='Admin').first()
			else:
				self.role = Role.objects(default=True).first()
		if self.avatar is None:
			self.avatar = "users/"+str(self.id)+".png"

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.p_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.p_hash, password)

	# Flask-Login integration
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

	def generate_confirmToken(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'],expiration)
		return s.dumps({'confirm':self.id})

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		self.save()
		return True

	def to_json(self):
		user = {
			'username':self.username,
			'last_seen':self.last_seen,
			'recipe_created': url_for('api.get_user_recipe', id=self.id, _external=True),
			'dish_created': url_for('api.get_user_dish', id=self.id, _external=True),
			'num_of_uploads': len(self.recipe) + len(self.dish)
		}
		return user

	@staticmethod
	def generate_fakes():
		import forgery_py
		import os
		from random import seed
		# insert admin
		admin = User(email=current_app.config['FY_ADMIN'],username='admin')
		admin.password = "1234"
		admin.confirmed = True
		admin.save()
	
		seed()
		path_to_fakes = url_for("static",filename="fakes/users")
		basedir = os.path.abspath(os.path.dirname(__file__))
		static_path = basedir+path_to_fakes
		for file in os.listdir(static_path):
			user = User(email=forgery_py.internet.email_address(),
						username=forgery_py.internet.user_name(True),
						confirmed=True, avatar=os.path.join("fakes/users",file))
			user.password = forgery_py.lorem_ipsum.word()
			try:
				user.save()
			except:
				current_app.logger.info("something went wrong...")

	def is_permitted(self, permission):
		return self.role is not None and self.role.is_permitted(permission)

	def is_admin(self):
		return self.is_permitted(Permission.ADMIN)
	
	def ping(self):
		self.last_seen = datetime.datetime.now
		self.save()

@login_manager.user_loader
def load_user(user_id):
	return User.objects(id=user_id).first()


class Dish(db.DynamicDocument):
	created = db.DateTimeField(default=datetime.datetime.now(), required=True)
	parent = db.ReferenceField('Recipe',required=True)
	prl = db.StringField(required=True)
	author = db.ReferenceField(User, reverse_delete_rule=CASCADE)
	comment = db.StringField(max_length=1200)

	def to_json(self):
		dish = {
			'created_time':self.created,
			'parent_recipe':url_for('api.get_recipe',recipe_id=self.parent.rid,_external =True),

			'img_link':url_for('static',filename=self.prl,_external =True),
			'author_id':self.author.id,
			'comment':self.comment
		}
		return dish

	@staticmethod
	def from_json(dish):
		prl = dish.get('prl')
		comment = dish.get('comment')
		if prl is None or comment is None:
			raise ValueError('field missing')
		dish = Dish(prl=prl,comment=comment)
		return dish


class Recipe(db.DynamicDocument):
	title = db.StringField(max_length=120, required=True)
	author = db.ReferenceField(User, reverse_delete_rule=CASCADE)
	desc = db.StringField(max_length=500, required=True)
	ing = db.StringField(max_length=1000, required=True)
	step = db.StringField(required=True)
	prl = db.StringField(required=True)
	rid = db.SequenceField(required=True)
	region = db.StringField(max_length=40, required=True)
	ming = db.StringField(max_length=40, required=True)
	kind = db.StringField(max_length=40, required=True)
	works = db.ListField(ReferenceField(Dish))
	ts  = db.DateTimeField(default=datetime.datetime.now)
	rate = db.DecimalField(default=0.0,precision=1)
	ppl = db.IntField(default=1)
	

	def to_json(self):
		recipe = {
			'url':url_for('api.get_recipe',recipe_id = self.rid, _external=True),
			'title':self.title,
			'author_id':self.author.id,
			'description':self.desc,
			'ingredients':self.ing,
			'steps':self.step,
			'img_url':url_for('static',filename=self.prl,_external =True),			
			'tags':[self.region,self.ming,self.kind],
			'date_created':self.ts,
			'rate':str(self.rate),
			'people_rated':self.ppl
		}
		return recipe

	@staticmethod
	def from_json_custom(recipe):
		title = recipe.get('title')
		desc = recipe.get('desc')
		ing = recipe.get('ing')
		prl = recipe.get('prl')
		step = recipe.get('step')
		tags = recipe.get('tags')

		if tags:
			region=tags[0]
			ming = tags[1]
			kind = tags[2]
		if title is None or\
			desc is None or step is None or\
			ing is None or prl is None or\
			region is None or ming is None or kind is None:
				raise ValueError('field missing')
		recipe = Recipe(title=title,ing=ing,prl=prl,desc=desc,step=step,
				region=region,ming=ming,kind=kind)
		return recipe


	@staticmethod
	def generate_fakes():
		import json
		from random import seed, randint
		import os

		seed()
		counts = User.objects.count()
		path_to_fakes = url_for("static",filename="fakes/recipes/recipes.json")
		basedir = os.path.abspath(os.path.dirname(__file__))
		static_path = basedir+path_to_fakes
		print (static_path)
		recipes = json.load(open(static_path,encoding='utf-8')).get('recipes')
		# print (recipes)
		for recipe in recipes:
			print (json.dumps(recipe))
			r = Recipe.from_json(json.dumps(recipe))
			
			users_count = User.objects.count()
			offset = randint(0,users_count-1)
			print (offset)
			user = User.objects[offset:].first()
			print (user.id)
			r.author = user

			r.save(force_insert=True)
