import secrets  # only used for a random hex
import os

from flask import request, render_template, redirect, flash, url_for, abort
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image  # part of Pillow (Python Imaging Library)

# import "db" and "app" defined in the __init__.py, and other modules from the package
# Note : for some reason the import of myblog package is flagged as an error in Pycharm
from myblog import app, db, bcrypt
from myblog.models import BlogPost, User
from myblog.forms import SignupForm, LoginForm, UpdateAccountForm, PostForm


# Handler for a GET request on url /hello returning a hardcoded string
@app.route('/hello')
def hello_handler():
    return 'Hello world'


# Handler using path parameters
@app.route('/users/<string:user_name>/posts/<int:post_id>')
def get_post_handler(user_name, post_id):
    return 'Fetching post ID %d for user %s' % (post_id, user_name)


# Handler restricting HTTP methods
@app.route('/users', methods=['GET', 'POST'])
def get_users_handler():
    return 'Getting users with method %s' % request.method


# Handler using a simple template
@app.route('/')
@app.route('/home')
def home_handler():
    return render_template('index.html', title="Home")


# Handler using a template looping on a custom list
@app.route('/friends')
def friends_handler():
    all_friends = [
        {'name': 'Bruce', 'hobby': 'tennis'},
        {'name': 'Peter', 'hobby': 'biology'},
        {'name': 'Damian', 'hobby': 'kung-fu', 'age': 15},
    ]
    return render_template('friends.html', title="Friends", friends=all_friends)


# Handler getting all posts in the database when called with GET
@app.route('/posts', methods=['GET'])
def get_posts_handler():
    # return all the posts from the DB
    all_posts = BlogPost.query.order_by(BlogPost.created_on).all()
    return render_template('posts.html', title="Posts", posts=all_posts)


# Handler to delete a blog post
@app.route('/posts/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post_handler(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author != current_user:   # we can also use: post.user_id != current_user.id
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('get_posts_handler'))


# Handler to create a post
# GET will access the creation page, and POST will create the post in the database
@app.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post_handler():
    form = PostForm()
    if form.validate_on_submit():
        # Add a post in the DB on POST (from the form submit button click)
        new_post = BlogPost(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Your post was successfully created.', 'success')
        return redirect('/posts')

    return render_template('create.html', title="New", form=form)


# Handler to edit a blog post
# GET will access the edition page, and POST will update the database
@app.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post_handler(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if current_user.id != post.user_id:
        # Not allowed to edit another user's post
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/posts')
    if request.method == 'GET':
        # pre-populate the title and content
        form.title.data = post.title
        form.content.data = post.content
    return render_template('edit.html', title="Edit", post=post, form=form)


# Handler to register a new user
@app.route('/signup', methods=['GET', 'POST'])
def signup_handler():
    # redirect to home if the user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('home_handler'))

    # build the form from the request
    form = SignupForm()
    # check if the method is POST and the provided data are valid
    if form.validate_on_submit():
        # create the user in DB with its password hash
        hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hash)
        db.session.add(user)
        db.session.commit()
        # send a temporary success alert to the frontend
        flash(f'Account created for {form.username.data}, please login.', 'success')
        return redirect(url_for('login_handler'))
 
    return render_template('signup.html', title="Signup", form=form)


# Handler to login with an existing user
@app.route('/login', methods=['GET', 'POST'])
def login_handler():
    # redirect to home if the user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('home_handler'))

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
            return redirect(next_page) if next_page else redirect(url_for('home_handler'))
        else:
            flash(f'Login failed : invalid credentials.', 'danger')

    return render_template('login.html', title="Login", form=form)


# Handler to logout with an existing user
@app.route('/logout')
def logout_handler():
    logout_user()
    return redirect(url_for('home_handler'))


def save_picture(picture):
    # create a name for the picture file
    hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(picture.filename)
    file_name = current_user.username + '_' + hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/images', file_name)
    # Resize the image with Pillow
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)
    # Save the file in the images folder
    i.save(picture_path)
    return file_name

# Handler to access the user account info (only available when logged in)
# The login_required decorator checks if the user is logged and if he is not he is redirected
# to the login page (specified in the login manager in __init__.py)
@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account_handler'))
    elif request.method == 'GET':
        # pre-populate the username and email
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_path = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_path = image_path, form=form)


@app.route('/reset_password')
def reset_password_handler():
    return 'TODO'
