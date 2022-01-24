from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask import render_template, redirect, request, session, flash

@app.route('/recipes/new')
def new_recipe():
    if 'id' not in session:
        return redirect('/')
    logged_in_user=User.get_one({'id':session['id']})
    all_recipes=logged_in_user.recipes
    print(all_recipes)
    return render_template('create.html', all_recipes=all_recipes)

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if 'id' not in session:
        return redirect('/')
    if not Recipe.validate(request.form):
        print('not valid')
        return redirect('/recipes/new')
    data={
        'name':request.form['name'],
        'description':request.form['description'],
        'under_over':request.form['under_over'],
        'instructions':request.form['instructions'],
        'date_made':request.form['date_made'],
        'user_id':session['id']
    }
    print(data)
    recipe_id=Recipe.create(data)
    return redirect('/dashboard')

@app.route('/recipes/<int:id>')
def get_recipe(id):
    if 'id' not in session:
        return ('/')
    logged_in_user=User.get_one({'id':session['id']})
    selected_recipe=Recipe.get_one({'id':id})
    return render_template('recipe.html', user=logged_in_user, recipe=selected_recipe)

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    if 'id' not in session:
        return redirect('/')
    Recipe.delete({'id':id})
    return redirect('/dashboard')

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'id' not in session:
        return redirect('/')
    selected_recipe=Recipe.get_one({'id':id})
    return render_template('update.html', recipe=selected_recipe)

@app.route('/recipes/update/<int:id>', methods=['POST'])
def update_recipe(id):
    if 'id' not in session:
        return redirect('/')
    if not Recipe.validate(request.form):
        return redirect(f"/recipes/edit/{id}")
    data={
        'id':id,
        'name':request.form['name'],
        'description':request.form['description'],
        'under_over':request.form['under_over'],
        'instructions':request.form['instructions'],
        'date_made':request.form['date_made']
    }
    Recipe.update(data)
    return redirect('/dashboard')

