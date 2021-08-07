import os

# To add config values to the Flask app, we can specify a config variable directly :
#     app.config['SECRET_KEY'] = '5jer0p5n1abl94g8hbh'
#
# Another approach is to group all the config variables into a config class.
# That allows to inherit from it and instantiate several instances of the app with different configs.
# The static variables of this class must be named like the config variables :
#     SECRET_KEY = '5jer0p5n1abl94g8hbh'


class Config:

    # Secret required to access data from the session
    # This should normally be provided via an env variable (not hardcoded in source code)
    SECRET_KEY = '5jer0p5n1abl94g8hbh'

    # Engine and path of the database
    # SQL-Alchemy can handle different database engines (MySQL, PostgreSQL, SQLite...)
    # Here we use SQLite that creates the DB in a local file in the current directory
    # When using mySQL or PostgreSQL the password and user are in the DB path, so it should
    # be provided via env variable instead
    SQLALCHEMY_DATABASE_URI = 'sqlite:///posts.db'  # 3 slashes is for relative path

    # Config for sending emails
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PWD')