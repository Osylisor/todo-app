from flask import Blueprint,  render_template, request, flash, redirect, url_for
from .models import  User
from flask_login import login_user, logout_user, current_user
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)


@auth.route('/', methods = ['GET', 'POST'])
def login():


    if(request.method == 'POST'):

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()


    

        #If this user exists...
        if(user):

            if check_password_hash(user.password, password):
                flash('You have logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please enter the correct password', category='error')
        else:
            flash('This email does not exists', category='error')



    return render_template('login.html')


@auth.route('/sign_up',  methods = ['GET', 'POST'])
def sign_up():

    if(request.method == 'POST'):

        #Get the data from the for when the user signs up
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_comfirm = request.form.get('password-comfirm')


        #Check if the user exists

        user = User.query.filter_by(email = email).first()

        if(user):
            flash('There is a user with this email, try another one', category='error')
        #Check for authentication errors when the user tries to sign up
        elif len(username) < 2:
            flash('Username is too short, please make sure it is longer than 1 character', 
            category='error')

        elif len(email) < 7:
            flash("Email is too short, please make sure that the email is more than 6 character",
             category='error')

        elif len(password) < 7:
            flash("Password has to be more than 6 characters in length", category='error')

        elif password != password_comfirm:
            flash('Please comfirm with the correct password')
        else:

            new_user_account = User(username = username,  email = email, 
                               password = generate_password_hash(password, method = "sha256"))

            login_user(new_user_account , remember = True)
            db.session.add(new_user_account)
            db.session.commit()
            flash('You have successfully created an account', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign-up.html')


@auth.route('/logout')
def logout():

    flash('You have been logged out successfully', category='success')
    logout_user()
    return redirect(url_for('auth.login'))
