import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


# Create a Flask object representing our webapp
app = Flask(__name__)

# A secret is required to access data from the session
# This should normally be provided via an env variable (not hardcoded in source code)
# The session allows the backend to store encrypted data.
# This data can be seen but not modified by the client without the secret key
app.config['SECRET_KEY'] = '5jer0p5n1abl94g8hbh'

# Setup the DB path
# SQL-Alchemy can handle different database engines (MySQL, PostgreSQL, SQLite...)
# Here we use SQLite that creates the DB in a local file in the current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'  # 3 slashes is for relative path

# Create the DB hadnler required to define the DB model and interact with the DB
db = SQLAlchemy(app)

# Bcrypt object to hash passwords and check a stored hash against a potential password from the user
bcrypt = Bcrypt(app)

# Login manager to handle user sessions
login_manager = LoginManager(app)
login_manager.login_view = 'users.login_handler'     # handler to redirect to for endpoints with login required
login_manager.login_message_category = 'info'  # set alert-info class to the message div when redirecting to login page 

# required setup for sending emails
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PWD')
if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    print('WARNING : Mail username/password should be set as env variables, the mail server will not be working.')
mail = Mail(app)

# import the routes so Flask knows about them when running the blog webapp with app.run()
from myblog.users.routes import users_blueprint
from myblog.posts.routes import posts_blueprint
from myblog.common.routes import common_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(common_blueprint)
