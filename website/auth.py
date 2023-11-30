from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='Success')
                login_user(user, remember=True)
            else:
                flash('Incorrect password, try again.', category='Error')
        else:
            flash('Email does not exist.', category='Error')
    return render_template("login.html", boolean="True")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='Error')

        if len(email) < 4:
            flash('Email must be greater than 4 chararacters.', category='Error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='Error')
        elif password1 != password2:
            flash('Passwords do not match.', category='Error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='Error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha1'))
            db.session.add(new_user)
            db.session.commit()
            flash('User added to database.', category="Success")
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")