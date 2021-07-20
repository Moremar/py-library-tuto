from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Create a Flask object representing our webapp
app = Flask(__name__)


# Handler for one or multiple route(s) returning a hardcoded string
@app.route('/')
@app.route('/home')
def hello():
    return 'Hello world'


# Handler using path parameters
@app.route('/users/<string:user_name>/posts/<int:post_id>')
def get_post(user_name, post_id):
    return 'Fetching post ID %d for user %s' % (post_id, user_name)


# Handler restricting HTTP methods
@app.route('/users', methods=['GET', 'POST'])
def get_users():
    return 'Getting users with method %s' % request.method


# Handler using a simple template
@app.route('/index')
def index_template():
    return render_template('index.html')


# Handler using a template looping on a custom list
@app.route('/friends')
def friends_template():
    all_friends = [
        {'name': 'Bruce', 'hobby': 'tennis'},
        {'name': 'Peter', 'hobby': 'biology'},
        {'name': 'Damian', 'hobby': 'kung-fu', 'age': 15},
    ]
    return render_template('friends.html', friends=all_friends)


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
    author = db.Column(db.String(20), nullable=False, default='N/A')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return 'BlogPost({}, {}, {}, {}, {})'.format(self.id, self.title, self.content, self.author, self.created_on)


# Handler getting all posts in the database when called with GET
# Insert a new blog post in the database when called with POST
@app.route('/posts', methods=['GET', 'POST'])
def get_posts():
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
    else:
        # return all the posts from the DB
        all_posts = BlogPost.query.order_by(BlogPost.created_on).all()
        return render_template('posts.html', posts=all_posts)


# Handler to delete a blog post
@app.route('/posts/delete/<int:post_id>')
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


# Handler to edit a blog post
# GET will access the edition page, and POST will update the database
@app.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    elif request.method == 'GET':
        return render_template('edit.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
