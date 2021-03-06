
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    user_data = User.get_user_by_id(data)
    return render_template('success.html', this_user = user_data)


@app.route('/new_account', methods=['POST'])
def process():
    data = {
        'first_name': request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':request.form['password']
    }
    if request.form['confirm_password'] != request.form['password']:
        flash('Password does not match')
        return redirect('/')
    if not User.check_if_email_in_system(data):
        flash('Email already taken!')
        return redirect('/')
    if not User.new_user_validation(data):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data['password'] = pw_hash
    #this is where I set the session, session transfers from page to page
    #inserting gives you back an ID
    session['user_id'] = User.save_user(data)
    # using session to stay logged in
    return redirect('/success')



@app.route('/signing_in', methods=['POST'])
def signing_in():
    data = {
        'email':request.form['email'],
    }
    user_in_db = User.get_user_by_email(data)
    
    if not user_in_db:
        flash('Invalid Email/Password')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/success')

@app.route('/signout')
def signout():
    session.clear()
    return redirect('/')