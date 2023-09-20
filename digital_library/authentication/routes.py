from flask import Blueprint, render_template, request, redirect,url_for,flash
from digital_library.models import User,db,check_password_hash
from digital_library.forms import UserSignupForm,UserSigninForm
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')
@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))   
    form = UserSignupForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password= form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            print(email,password)

            user = User(email, first_name, last_name, id='', password = password)
            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'user-created')

            return redirect(url_for('site.home'))
        elif request.method == 'POST' and (not form.validate_on_submit()):

            flash('Invalid Form Data. Please Try again.', 'form-failed')
    except:
        raise Exception('Invalid Form Data: Please Check your form')
    return render_template('signup.html', form=form)
    
@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))  
    form=UserSigninForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            logged_user = User.query.filter(User.email == email).first()

            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in: Via Email/Password', 'auth-success')

                return redirect(url_for('site.home'))
            else:
                flash('Your Email/Password is incorrect', 'auth-failed')

                return redirect(url_for('auth.signin'))

        elif request.method == 'POST' and (not form.validate_on_submit()):

            flash('Invalid Form Data. Please Try again', 'form-failed')
            
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('signin.html', form=form)

@auth.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('site.home'))    