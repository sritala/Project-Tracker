from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    # mahdolliset validoinnit

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "No such username or password")

    print("Käyttäjä " + user.name + " tunnistettiin")
    login_user(user)
    return redirect(url_for("index"))    

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index")) 

#Rekisteröinti

@app.route("/auth/register", methods=["GET"])
def auth_register_form():
    return render_template("auth/registration.html", form=RegisterForm())

@app.route("/auth/register", methods=["POST"])
def auth_register():
    form = RegisterForm(request.form)
    

#Jos salasanat ei täsmää

    if form.password.data != form.passwordAgain.data: 
        return render_template("auth/registration.html", form=form, error="Passwords don't match")

    if not form.validate():
        return render_template("auth/registration.html", form=form)

    user = User(form.name.data)
    user.username = form.username.data
    user.password = form.password.data
  
    db.session().add(user)
    db.session().commit()

    return redirect(url_for("auth_login"))