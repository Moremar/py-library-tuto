from myblog.models import User, BlogPost

# This is a simple script to show the content of all tables in the DB

# print all users
users = User.query.all()
print('Users:', *users, sep='\n    ')

# print all posts
posts = BlogPost.query.all()
print('\nPosts:', *posts, sep='\n    ')
