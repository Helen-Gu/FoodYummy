from . import main
from ..models import Recipe, Dish, User
from flask_login import login_required, current_user
from .forms import EditProfileForm, EditProfileAdminForm
from werkzeug import secure_filename
from flask import Flask, request, render_template, session,current_app, flash, redirect, url_for, jsonify
from flask_mail import Message
from app import mail
import os
from ..decorators import admin_only


@main.route('/', methods=['GET','POST'])
def index():
    
    if (request.method == "POST"):
        region=request.form["region"]
        ming=request.form["ming"]
        if (region=="All" and ming=="All"):
            recipe = Recipe.objects(kind=request.form["kind"])
        elif (ming=="All"):
            recipe = Recipe.objects(region=request.form["region"],kind=request.form["kind"])
        elif (region=="All"):
            recipe = Recipe.objects(ming=request.form["ming"],kind=request.form["kind"])
        else:
            recipe = Recipe.objects(region=request.form["region"],ming=request.form["ming"],kind=request.form["kind"])
        return render_template("homepage.html", r=recipe)
    else:
        recipe = Recipe.objects(kind="meal")
        return render_template("homepage.html", r=recipe)

@main.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        msg = Message(current_app.config['FY_MAIL_SUBJECT_PREFIX'] + \
            " comment", sender=current_app.config['FY_MAIL_SENDER'],\
             recipients=[current_app.config['FY_ADMIN']])
        msg.body = render_template('auth/email/contact.txt', form=request.form)
        mail.send(msg)
        return redirect(url_for("main.index"))
    return redirect(url_for("main.index"))

@main.route('/myspace', methods=['GET','POST'])
@login_required
def dashboard():
    recipe = Recipe.objects.order_by('-ts')
    dish = Dish.objects.order_by('-created')
    return render_template("myspace.html",r=recipe,d=dish,title="My Space")

@main.route("/recipe/<int:recipe_id>", methods=['GET','POST'])
def recipe(recipe_id):
    id = int(recipe_id)
    recipe = Recipe.objects(rid=id).first()
    if (request.method == "POST"):
        author=recipe.author
        value = int(request.form["rating"])
        rate = recipe.rate
        ppl = recipe.ppl
        new_rate = (rate * ppl +value) / (ppl+1)
        Recipe.objects(prl=recipe.prl).update_one(set__rate=new_rate)
        Recipe.objects(prl=recipe.prl).update_one(inc__ppl=1)
        return render_template("recipe.html", number=new_rate, r=recipe)
    return render_template("recipe.html", number = "{0:.1f}".format(recipe.rate), r=recipe)


def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

@main.route("/recipe-upload",methods=['GET','POST'])
@login_required
def uploadRecipe():
    if (request.method == "POST"):
        file = request.files['prl']
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER_RECIPE'], filename))
        path=str(os.path.join("images/recipe", filename))
        
        recipe = Recipe(author=current_user._get_current_object(),
            prl=path,title=request.form["title"], desc=request.form["desc"],
            ing=request.form["ingre"],step=request.form["steps"],
            region=request.form["origin"],ming=request.form["main-ing"],
            kind=request.form["category"])
        # recipe.img.put(file, content_type=file.content_type)
        recipe.save()
        current_user.recipe.append(recipe)
        current_user.save()
        return redirect(url_for('main.loadRecipe'))
    return render_template("uploadrecipe.html",title="Upload Recipe")

@main.route("/recipe/<recipe_id>/dish-upload",methods=['GET','POST'])
@login_required
def uploadDish(recipe_id):
    if (request.method == "POST"):
        file = request.files['prl']
        filename = secure_filename(file.filename)
        basedir = os.path.abspath(os.path.dirname(__file__))
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER_DISH'], filename))
        path=str(os.path.join("images/dish", filename))
        recipe = Recipe.objects(rid=recipe_id).first()
        dish = Dish(parent=recipe,comment=request.form["message"],prl=path)
        #dish.img.put(file, content_type=file.content_type)
        dish.save()
        current_user.dish.append(dish)
        current_user.save()
        return redirect(url_for('main.loadDish'))
    return render_template("uploaddish.html",title="Upload Dish")
        
@main.route("/edit-profile",methods=['GET','POST'])
@login_required
def editProfile():
    form = EditProfileForm(request.form)
    current_app.logger.info(request.form)
    link = str(current_app.config['UPLOAD_FOLDER_USER']+current_user.avatar)
    if (request.method == 'POST' and form.validate()):
        avatar = request.files['avatar']
        if avatar:
            if allowed_file(avatar.filename):
                filename = secure_filename(avatar.filename)
                current_app.logger.info(link)
                avatar.save(link)
            else:
                return "failed"
        current_user.username = form.new_name.data
        current_user.password = form.password.data
        current_user.save()
        flash('You has successfully updated your profile!')
        return redirect(url_for('main.dashboard'))
                    
    return render_template("editprofile.html",form=form,avatar=link)

@main.route("/edit-profile/admin",methods=['GET','POST'])
@login_required
@admin_only
def editProfileAdmin():
    if (request.method == 'POST'):
        user = User.objects(id=int(request.form['user'])).first()
        form = EditProfileAdminForm(user=user)
        if form.validate():
            user = User.object(id=int(request.form.user)).first()
            if form.email.data:
                user.email = form.email.data
            if form.username.data:
                user.username = form.username.data
            if form.password.data:
                user.password = form.password.data
            user.confirmed = form.confirmed.data
            user.role = Role.objects(permissions=form.role.data).first()
            user.save()
            return jsonify(status="success")
        else:
            errors = {"status":"fail"}
            for field in form:
                if field.errors:
                    for error in field.errors:
                        errors[field.name] = error
            return jsonify(errors)
    if (request.method == 'GET'):
        request_id = request.args.get('id')
        if request_id:
            user = User.objects(id=int(request_id)).first()
            form = EditProfileAdminForm(user=user)
            return render_template("editprofile-admin-form.html",form=form,user=user)
        users = User.objects
        return render_template("editprofile-admin.html",users=users)        



                        
@main.route("/myrecipe",methods=['GET','POST'])
@login_required
def loadRecipe():
    recipe = current_user.recipe
    return render_template("myrecipe.html",title="My Recipe",r=recipe)

@main.route("/mydish",methods=['GET','POST'])
@login_required
def loadDish():
    dish = current_user.dish
    return render_template("mydish.html",title="My Dish",r=dish)
