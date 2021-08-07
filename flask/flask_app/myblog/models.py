from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer

from myblog import db, login_manager


# For the login manager to be able to manage the session, it needs :
#  - the below function with decorator to know how to get a user in DB
#  - the DB user model to have some specific fields (is_active, is_authenticated...)
#    these can be done by extending the UserMixin class
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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


class User(db.Model, UserMixin):
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

    def generate_reset_token(self):
        secret_key = current_app.config['SECRET_KEY']
        serializer = URLSafeTimedSerializer(secret_key, salt='RESET')
        return serializer.dumps({ 'user_id': self.id })

    @staticmethod
    def verify_reset_token(token):
        secret_key = current_app.config['SECRET_KEY']
        serializer = URLSafeTimedSerializer(secret_key, salt='RESET')
        try:
            user_id = serializer.loads(token, max_age=600)['user_id']  # expire after 10min
        except Exception as e:
            return None
        return User.query.get(user_id)
