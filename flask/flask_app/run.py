from myblog import create_app

# For a better split of the code, we run the webapp from this run.py script.
# The actual webapp code is in its own package.
# The "db" and "app" variable are defined in the __init__.py of the package so they are accessible to
# the outside (like this script) and to all modules inside the package.
# The package contains a specific module for :
#  - the routes registered in the webapp
#  - the forms used in the web pages
#  - the model of the DB

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
