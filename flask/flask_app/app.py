from flask import Flask, request, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from forms import SignupForm, LoginForm


# Create a Flask object representing our webapp
app = Flask(__name__)

# A secret is required to access data from the session
# The session allows the backend to store encrypted data.
# This data can be seen but not modified by the client without the secret key
app.config['SECRET_KEY'] = '5jer0p5n1abl94g8hbh'


# Handler for one or multiple route(s) returning a hardcoded string
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


# Setup the DB path
# SQL-Alchemy can handle different database engines (MySQL, PostgreSQL, SQLite...)
# Here we use SQLite that creates the DB in a local file in the current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'  # 3 slashes is for relative path
db = SQLAlchemy(app)


# Create the model for the blog posts table in the DB
# The types are dynamically attached to the SQLAlchemy object so python does not detect them
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # Field defined as foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'BlogPost({self.id}, {self.title}, {self.content}, {self.user_id}, {self.created_on})'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password_hash = db.Column(db.String(60), nullable=False)

    # 1-to-many relationship : define a relationship in the parent and a foreign key in the child
    # calling user.posts will actually run a query to fetch the posts
    # calling post.author will get the User object associated to the foreign key
    # the 'lazy' will load the posts for a user only when requested
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __repr__(self):
        return f'User({self.id}, {self.username}, {self.email}, {self.image_file})'


# Handler getting all posts in the database when called with GET
@app.route('/posts', methods=['GET'])
def get_posts_handler():
    # return all the posts from the DB
    all_posts = BlogPost.query.order_by(BlogPost.created_on).all()
    return render_template('posts.html', title="Posts", posts=all_posts)


# Handler to delete a blog post
@app.route('/posts/delete/<int:post_id>')
def delete_post_handler(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


# Handler to create a post
# GET will access the creation page, and POST will create the post in the database
@app.route('/posts/create', methods=['GET', 'POST'])
def create_post_handler():
    if request.method == 'POST':
        # Add a post in the DB on POST (from the form submit button click)
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        # Create DB object
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    elif request.method == 'GET':
        return render_template('create.html', title="New")


# Handler to edit a blog post
# GET will access the edition page, and POST will update the database
@app.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post_handler(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    elif request.method == 'GET':
        return render_template('edit.html', title="Edit", post=post)


# Handler to register a new user
@app.route('/signup', methods=['GET', 'POST'])
def signup_handler():
    # build the form from the request
    form = SignupForm()
    # check if the method is POST and the provided data are valid
    if form.validate_on_submit():
        # send a temporary success alert to the frontend
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home_handler'))
    return render_template('signup.html', title="Signup", form=form)


# Handler to login with an existing user
@app.route('/login', methods=['GET', 'POST'])
def login_handler():
    # build the form from the request
    form = LoginForm()
    # check if the method is POST and the provided data are valid
    if form.validate_on_submit():
        # TODO proper validation against backend
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            # send a temporary success alert to the frontend
            flash(f'Logged as {form.email.data}!', 'success')
            return redirect(url_for('home_handler'))
        else:
            flash(f'Login failed : invalid credentials.', 'danger')
    return render_template('login.html', title="Login", form=form)


@app.route('/reset_password')
def reset_password_handler():
    return 'TODO'


if __name__ == '__main__':
    app.run(debug=True)
