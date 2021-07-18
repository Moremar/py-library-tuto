from flask import Flask, request, render_template

# Create a Flask object representing our webapp
app = Flask(__name__)


# Handler for one or multiple route(s) returning a hardcoded string
@app.route('/')
@app.route('/home')
def hello():
    return 'Hello world'


# Handler using path parameters
@app.route('/users/<string:user_name>/posts/<int:post_id>')
def get_post(user_name, post_id):
    return 'Fetching post ID %d for user %s' % (post_id, user_name)


# Handler restricting HTTP methods
@app.route('/users', methods=['GET', 'POST'])
def get_users():
    return 'Getting users with method %s' % request.method


# Handler using a simple template
@app.route('/index')
def index_template():
    return render_template('index.html')


# Handler using a template looping on a custom list
@app.route('/friends')
def friends_template():
    all_friends = [
        {'name': 'Bruce', 'hobby': 'tennis'},
        {'name': 'Peter', 'hobby': 'biology'},
        {'name': 'Damian', 'hobby': 'kungfu', 'age': 15},
    ]
    return render_template('friends.html', friends=all_friends)


if __name__ == '__main__':
    app.run(debug=True)
