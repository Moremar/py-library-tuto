from myblog import app

# For a better split of the code, we only have this run.py script run the webapp.
# The actual webapp code is in its own package.
# The "db" and "app" variable are defined in the __init__.py of the package so they are accessible to
# the outside (like this script) and to all modules inside the package.
# The package contains a specific module for :
#  - the routes registered in the webapp
#  - the forms used in the web pages
#  - the model of the DB


if __name__ == '__main__':
    app.run(debug=True)
