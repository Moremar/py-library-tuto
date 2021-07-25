from datetime import datetime

from myblog import db


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
