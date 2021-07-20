from app import db
from app import BlogPost

# This code can be ran to create the DB (this should be done once, and not via the website)
# It also shows several commands to interact with objects in the DB, for example the CRUD
# commands used by URL handlers of the Flask website to create/read/update/delete blog posts.

# create the DB
db.create_all()

# create DB objects and add them in the current session
# The objects are created using the BlogPost model
db.session.add(BlogPost(title='Blog post 1', content='This is the content', author='Tom'))
db.session.add(BlogPost(title='Blog post 2', content='This is the content 2'))

# persist the changes of the session to the DB
db.session.commit()

# access all elements of a table in DB
res = BlogPost.query.all()
print(res)

# filter the result
res = BlogPost.query.filter_by(title='Blog post 1').all()
print(res)

# get a post by ID
res = BlogPost.query.get(1)
print(res)

# delete a post by ID
db.session.delete(BlogPost.query.get(1))
db.session.commit()
print(BlogPost.query.get(1))

# update a post by ID
post = BlogPost.query.get(2)
post.author = 'Patrick'
db.session.commit()
print(BlogPost.query.get(2))
