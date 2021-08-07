from flask import render_template, Blueprint


common_blueprint = Blueprint('common', __name__)


# Handler for a GET request on url /hello returning a hardcoded string
@common_blueprint.route('/hello')
def hello_handler():
    return 'Hello world'


# Handler using a simple template
@common_blueprint.route('/')
@common_blueprint.route('/home')
def home_handler():
    return render_template('index.html', title="Home")


# Dummy handler using a template looping on a custom list
@common_blueprint.route('/friends')
def friends_handler():
    all_friends = [
        {'name': 'Bruce', 'hobby': 'tennis'},
        {'name': 'Peter', 'hobby': 'biology'},
        {'name': 'Damian', 'hobby': 'kung-fu', 'age': 15},
    ]
    return render_template('friends.html', title="Friends", friends=all_friends)
