from flask import request, render_template, redirect, flash, url_for, Blueprint
from flask_login import login_user, logout_user, current_user, login_required

# import "db" and "app" defined in the __init__.py, and other modules from the package
# Note : for some reason the import of myblog package is flagged as an error in Pycharm
from myblog import db, bcrypt, mail
from myblog.models import User
from myblog.users.forms import SignupForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from myblog.users.utils import save_picture, send_reset_email


# The name "users" used for the blueprint is the prefix to use in all calls of url_for()
users_blueprint = Blueprint('users', __name__)


# Handler to register a new user
@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup_handler():
    # redirect to home if the user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('common.home_handler'))

    # build the form from the request
    form = SignupForm()
    # check if the method is POST and the provided data are valid
    if form.validate_on_submit():
        # create the user in DB with its password hash
        pwd_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=pwd_hash)
        db.session.add(user)
        db.session.commit()
        # send a temporary success alert to the frontend
        flash(f'Account created for {form.username.data}, please login.', 'success')
        return redirect(url_for('users.login_handler'))

    return render_template('signup.html', title="Signup", form=form)


# Handler to login with an existing user
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login_handler():
    # redirect to home if the user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('common.home_handler'))

    # build the form from the request
    form = LoginForm()
    # check if the method is POST and the provided data are valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            # login the user using Flask-Login extension
            login_user(user, remember=form.remember_me.data)
            flash(f'Logged as {form.email.data}!', 'success')
            # if there is a next page in the query, redirect to it (in case of login required redirect)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('common.home_handler'))
        else:
            flash(f'Login failed : invalid credentials.', 'danger')

    return render_template('login.html', title="Login", form=form)


# Handler to logout with an existing user
@users_blueprint.route('/logout')
def logout_handler():
    logout_user()
    return redirect(url_for('common.home_handler'))


# Handler to access the user account info (only available when logged in)
# The login_required decorator checks if the user is logged and if he is not he is redirected
# to the login page (specified in the login manager in __init__.py)
@users_blueprint.route('/account', methods=['GET', 'POST'])
@login_required
def account_handler():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            # save the file in the images folder
            file_name = save_picture(form.picture.data)
            # Update the DB with this file
            current_user.image_file = file_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account_handler'))
    elif request.method == 'GET':
        # pre-populate the username and email
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_path = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_path=image_path, form=form)


# password reset step 1 : send an email to the address with a link for password reset
@users_blueprint.route('/reset_password', methods=['GET', 'POST'])
def request_reset_handler():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'success')
        return redirect(url_for('users.login_handler'))
    return render_template('request_reset.html', title='Request Reset', form=form)


# password reset step 2 : check the token and let the user reset his password
@users_blueprint.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_password_handler(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('The provided token is invalid or expired.', 'warning')
        return redirect(url_for('users.request_reset_handler'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        pwd_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password_hash = pwd_hash
        db.session.commit()
        flash(f'Your password has been updated, please login.', 'success')
        return redirect(url_for('users.login_handler'))
    return render_template('reset_password.html', title='Reset Password', form=form)
