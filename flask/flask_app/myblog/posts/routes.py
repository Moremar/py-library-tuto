from flask import request, render_template, redirect, flash, url_for, abort, Blueprint
from flask_login import current_user, login_required

# import "db" and "app" defined in the __init__.py, and other modules from the package
# Note : for some reason the import of myblog package is flagged as an error in Pycharm
from myblog import db
from myblog.models import BlogPost, User
from myblog.posts.forms import PostForm


# The name "posts" used for the blueprint is the prefix to use in all calls of url_for()
posts_blueprint = Blueprint('posts', __name__)


# Handler getting all posts in the database when called with GET
@posts_blueprint.route('/posts', methods=['GET'])
def get_posts_handler():
    # optional parameters
    user_id = request.args.get('user', -1, type=int)
    page = request.args.get('page', 1, type=int)
    if user_id != -1:
        # return all posts from the specified user paginated by pages of 3 posts
        user = User.query.get_or_404(user_id)
        posts = BlogPost.query \
            .filter_by(user_id=user_id) \
            .order_by(BlogPost.created_on.desc()) \
            .paginate(per_page=3, page=page)
    else:
        # return all the posts from the DB paginated by pages of 3 posts
        user = None
        posts = BlogPost.query \
            .order_by(BlogPost.created_on.desc()) \
            .paginate(per_page=3, page=page)
    return render_template('posts.html', title="Posts", posts=posts, user=user)


# Handler to delete a blog post
@posts_blueprint.route('/posts/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post_handler(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author != current_user:  # we can also use: post.user_id != current_user.id
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('posts.get_posts_handler'))


# Handler to create a post
# GET will access the creation page, and POST will create the post in the database
@posts_blueprint.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post_handler():
    form = PostForm()
    if form.validate_on_submit():
        # Add a post in the DB on POST (from the form submit button click)
        new_post = BlogPost(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Your post was successfully created.', 'success')
        return redirect('/posts')

    return render_template('create.html', title="New", form=form)


# Handler to edit a blog post
# GET will access the edition page, and POST will update the database
@posts_blueprint.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post_handler(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if current_user.id != post.user_id:
        # Not allowed to edit another user's post
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/posts')
    if request.method == 'GET':
        # pre-populate the title and content
        form.title.data = post.title
        form.content.data = post.content
    return render_template('edit.html', title="Edit", post=post, form=form)
