import os
import requests
import urllib.parse

from flask import flash, redirect, render_template, request, session
from functools import wraps

from PIL import Image

# combining answers from Stevoisiak and getup8 on stack overflow
# https://stackoverflow.com/questions/23064549/get-date-and-time-when-photo-was-taken-from-exif-data-using-pil
# get the datetime from when an image was created
def get_date_taken(path):
    im = Image.open(path)
    exif = im.getexif()
    return exif.get(306)

def broadcast(message, code=400):
    """Render message as an broadcast to user."""
    # Format broadcast into flash()
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    # detailed version of flash
    # return flash("Error Code " + str(code) + ": " + message)

    return flash(message)


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

