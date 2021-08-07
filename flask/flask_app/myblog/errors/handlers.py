from flask import Blueprint, render_template

errors_blueprint = Blueprint('errors', __name__)


# decorator for error handlers
@errors_blueprint.app_errorhandler(404)
def error_404(error):
    # In flask we can return a 2nd parameter for the status (default to 200 so not specified in valid routes)
    return render_template('errors/404.html'), 404


@errors_blueprint.app_errorhandler(403)
def error_403(error):
    # In flask we can return a 2nd parameter for the status (default to 200 so not specified in valid routes)
    return render_template('errors/403.html'), 403


@errors_blueprint.app_errorhandler(500)
def error_500(error):
    # In flask we can return a 2nd parameter for the status (default to 200 so not specified in valid routes)
    return render_template('errors/500.html'), 500
