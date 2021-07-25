from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create a Flask object representing our webapp
app = Flask(__name__)

# A secret is required to access data from the session
# The session allows the backend to store encrypted data.
# This data can be seen but not modified by the client without the secret key
app.config['SECRET_KEY'] = '5jer0p5n1abl94g8hbh'

# Setup the DB path
# SQL-Alchemy can handle different database engines (MySQL, PostgreSQL, SQLite...)
# Here we use SQLite that creates the DB in a local file in the current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'  # 3 slashes is for relative path

# Create the DB hadnler required to define the DB model and interact with the DB
db = SQLAlchemy(app)

# import the routes so Flask knows about them when running the blog webapp with app.run()
from myblog import routes
