from myblog import db
from myblog.models import BlogPost, User

# This script shows the commands to interact with the database using the SQLAlchemy model classes.
# - DB deletion
# - DB creation
# - CRUD operations
# It is not part of the webapp, but similar commands are used in the webapp routes to create/update/delete resources.


# drop existing DB
db.drop_all()

# create the DB tables from the Python model classes
db.create_all()

# create DB objects and add them in the current session
# The objects are created using the User and BlogPost models
user1 = User(username='user1', email='user1@blog.com', password_hash='hash1')
user2 = User(username='user2', email='user2@blog.com', password_hash='hash2')
db.session.add(user1)
db.session.add(user2)
user1, user2 = User.query.all()

post1 = BlogPost(title='Blog post 1', content='This is the content of post 1', user_id=user1.id)
post2 = BlogPost(title='Blog post 2', content='This is the content of post 2', user_id=user2.id)
post3 = BlogPost(title='Blog post 3', content='This is the content of post 3', user_id=user2.id)
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

# persist the changes of the session to the DB
db.session.commit()

# access all elements of a table in DB
res = User.query.all()
print('Users:', *res)
res = BlogPost.query.all()
print('Posts:', *res)

# filter the result
res = BlogPost.query.filter_by(user_id=1).all()
print('Filtered by user 1:', *res)

# get a post by ID
post1 = BlogPost.query.get(1)
print('Post by ID 1:', post1)

# Use the 'fake' fields of the relationship
user2 = User.query.get(2)
post2 = BlogPost.query.get(2)
print('Posts of user 2:', user2.posts)
print('Author of post 2:', post2.author)

# delete a post by ID
db.session.delete(BlogPost.query.get(1))
db.session.commit()
print('Post 1 after deletion:', BlogPost.query.get(1))

# update a post by ID
post = BlogPost.query.get(2)
post.title += '!!!!'
db.session.commit()
print('Post 2 after update:', BlogPost.query.get(2))
