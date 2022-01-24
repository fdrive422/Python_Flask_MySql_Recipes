from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe   #added this import for recipe data needed for the get_all class
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template, redirect, request, session, flash

@app.route('/')
def index():
    if 'id' in session:
        return redirect('/dashboard')

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    user_in_db=User.get_by_email({'email':request.form['email']})
    if not user_in_db:
        flash("*invalid email address", "login_errors")
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("*password incorrect", "login_errors")
        return redirect('/')

    session['id']=user_in_db.id
    return redirect('/dashboard')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/')
    pass_hash=bcrypt.generate_password_hash(request.form['password'])
    data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password': pass_hash
    }
    print(data)
    user_id=User.create(data)
    session['id']=user_id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect('/')

    logged_in_user=User.get_one({'id':session['id']})
    all_recipes=Recipe.get_all()
    return render_template('dashboard.html', user=logged_in_user, all_recipes=all_recipes)

@app.route('/logout')
def logout():
    session.clear()
    flash('Successfully logged out', 'logout')
    return redirect('/')