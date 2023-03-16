from flask_app.models.user import User
from flask_app import app
from flask import render_template, request, redirect,session,flash
from flask_bcrypt import Bcrypt
bcrypt= Bcrypt(app)


@app.route("/")
def show_form():
    return render_template("index.html")

@app.route("/register",methods=['POST'])
def create():
    if not User.validate_user(request.form):
        return redirect("/")

    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    user_data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':hashed_pw
    }
    id=User.save(user_data)
    session['user_id']=id
    session['first_name']=request.form['first_name']
    session['last_name']=request.form['last_name']
    return redirect("/dashboard")

@app.route("/login",methods=['POST'])
def login():
    user=User.get_by_email(request.form['email'])
    if user == None:
        flash("Invalid email or password!","log")
        return redirect("/")
    password_valid = bcrypt.check_password_hash(user['password'], request.form['password'])
    if password_valid == False:
        flash("Invalid email or password!","log")
        return redirect("/")
    session['user_id']= user['id']
    session['first_name']= user['first_name'] 
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


