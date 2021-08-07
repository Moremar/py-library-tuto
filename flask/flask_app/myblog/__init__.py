from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from myblog.config import Config


# Create the DB handler required to define the DB model and interact with the DB
db = SQLAlchemy()

# Bcrypt object to hash passwords and check a stored hash against a potential password from the user
bcrypt = Bcrypt()

# Login manager to handle user sessions
login_manager = LoginManager()
login_manager.login_view = 'users.login_handler'     # handler to redirect to for endpoints with login required
login_manager.login_message_category = 'info'  # set alert-info class to the message div when redirecting to login page 

# Mail manager
mail = Mail()

# import the routes so Flask knows about them when running the blog webapp with app.run()
from myblog.users.routes import users_blueprint
from myblog.posts.routes import posts_blueprint
from myblog.common.routes import common_blueprint
from myblog.errors.handlers import errors_blueprint


def create_app(config_class=Config):
    # Create a Flask object representing our webapp
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Check the config if needed
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        print('WARNING : MAIL_USERNAME and MAIL_PASSWORD env variables missing, the mail server will not be working.')

    # Initialize extensions
    # They are created outside of the create_app method and are app-independent
    # Here we bind them to our specific app object
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # register all blueprints for this app
    app.register_blueprint(users_blueprint)
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(common_blueprint)
    app.register_blueprint(errors_blueprint)

    return app