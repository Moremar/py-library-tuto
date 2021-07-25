from myblog import db

# This can be run to destroy and recreate from scratch the database from the model.
# It is typically used only once before the launch of the webapp.

# drop existing DB
db.drop_all()

# create the DB tables from the Python model classes
db.create_all()
