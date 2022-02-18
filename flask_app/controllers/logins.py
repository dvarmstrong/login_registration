from flask import flash
from flask_app import app 
from flask import render_template, session, redirect, request 
from flask_app.models.login import User  
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register/user', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    # create the password hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data ={
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }

    user_id = User.save(data)
    #store user id into session
    session['user_id'] = user_id
    return redirect('/success')


@app.route('/success')
def show_user():
    return render_template('success.html', user_id = session['user_id'])

@app.route('/login', methods=['POST'])
def login():
    # see if username exsits in the database 
    data = { "email" : request.form["email"]}
    user_in_db = User.get_by_email(data)

    #if user is not registered in the database 
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    # if the passwords match , we set the user_id into sessions 

    session['user_id'] = user_in_db.id
    return redirect('/success')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/success') #not understanding this
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id' : session['user_id']
    }
    return render_template('success.html', user=User.get_by_id(data))