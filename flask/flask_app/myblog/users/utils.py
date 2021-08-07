import secrets  # only used for a random hex
import os

from flask import current_app, url_for
from flask_login import current_user
from flask_mail import Message
from PIL import Image  # part of Pillow (Python Imaging Library)

# import "db" and "app" defined in the __init__.py, and other modules from the package
# Note : for some reason the import of myblog package is flagged as an error in Pycharm
from myblog import mail


def save_picture(picture):
    # create a name for the picture file
    hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(picture.filename)
    file_name = current_user.username + '_' + hex + file_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', file_name)
    # Resize the image with Pillow
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)
    # Save the file in the images folder
    i.save(picture_path)
    return file_name


# Helper function to send an email to a user with a password reset link
def send_reset_email(user):
    token = user.generate_reset_token()
    msg_body = f'''\
To reset your password, click on the following link:
{url_for('users.reset_password_handler', token=token, _external=True)}

If you didn't make this request, you can just ignore this email.
'''
    msg = Message(subject='Password reset request',
                  recipients=[user.email],
                  body=msg_body,
                  sender='noreply@demo.com')
    mail.send(msg)
