import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
from datetime import datetime
import logging

from helpers import broadcast, login_required, get_date_taken

# Set the upload folder and allowed extensions for downloads
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'gif'}

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Set folder to store images in
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///photocloud.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    # get a dictionary of image paths for the current user from db
    image_info = db.execute("SELECT * FROM images WHERE user_id = :id ORDER BY create_dt ASC, upload_dt DESC", id=session["user_id"])

    # send the dictionary over when rendering html
    return render_template("index.html", image_info = image_info)



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    # if user reached route via POST
    if request.method == "POST":

        # initialize variables for the username, password and password confirmation from the registration form

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # if no username is submitted, apologize
        if not username:
            broadcast("Please provide a username.")
            return render_template("register.html")

        # if no password is submitted, apologize
        elif not password:
            broadcast("Please provide a password.")
            return render_template("register.html")

        # if no password confirmation is submitted, apologize
        elif not confirmation:
            broadcast("Please confirm your password.")
            return render_template("register.html")

        # check the username against the database to make sure it hasn't already been inputted
        elif len(db.execute("SELECT * FROM users WHERE username = ?", username)) != 0:
            broadcast("Username is already in use.")
            return render_template("register.html")

        # check confirmation password and inputted passwords match
        elif not confirmation == password:
            broadcast("Passwords need to match.")
            return render_template("register.html")

        else:

            # generate password hash and input the new username and password into the database
            password_hash = generate_password_hash(password, "sha256")
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", username, password_hash)

            # redirect user back to their home page
            return redirect("/")

    # if user reached route via GET
    else:
        return render_template("register.html")



# Modified from flask documentation
# https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
@app.route("/upload_files", methods=["GET", "POST"])
@login_required
def upload_files():

    # if user reached route via POST
    if request.method == "POST":

        # get a list of files from the input form
        files = request.files.getlist("file")

        # check to make sure there's a file uploaded
        for file in files:

            # check to make sure there's a file uploaded
            if file.filename == '':
                broadcast("Please select an image or images.")
                return render_template("upload_files.html")

            # check to make sure file has appropriate extension
            elif not allowed_file(file.filename):
                broadcast("Only upload images with .png, .jpg, .jpeg or .gif extensions.")
                return render_template("upload_files.html")


            elif file:
                # grab the name of the file as it's uploaded
                filename = secure_filename(file.filename)

                # combine the name of the file with the folder it should be uploaded in
                # (get the path)
                path_input = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # get path before extension

                # run through the original path
                for character in range(len(path_input)):

                    # look right before the extension
                    if path_input[character] == ".":

                        # save the path input as a new variable without extension
                        path_input_noex = path_input[:character]

                # check against database for duplicates
                used_paths = db.execute("SELECT location FROM images WHERE location LIKE ?", path_input_noex + '%');
                if used_paths:

                    # loop through existing file paths
                    for i in used_paths:

                        # if the current file already exists, add a duplicate number
                        if path_input == i['location']:

                            # count how many duplicates already exist (not counting the number after file name)
                            duplicate_count = db.execute("SELECT count(location) FROM images WHERE location LIKE ?",
                                                            path_input_noex + '%')[0]['count(location)'];

                            # run through the original path
                            for character in range(len(path_input)):

                                # look right before the extension
                                if path_input[character] == ".":

                                    # add the duplicate number to the file path right before the extension
                                    path = path_input[:character] + str(duplicate_count) + path_input[character:]

                                    # log the path of the saved file
                                    app.logger.info("File saved to: " + path)

                # otherwise if no duplicates keep original path / filename
                else:
                    path = path_input

                    # log the path of the saved file
                    app.logger.info("Saved to: " + path)

                # actually save the file to the path
                file.save(path)

                # get the date the image was created / taken if it exists
                date_taken = str(get_date_taken(path))

                # get the current datetime
                now = datetime.now()
                dt_string = now.strftime("%d-%m-%Y %H:%M:%S")

                # record image with user id in the images database
                db.execute("INSERT INTO images(user_id, location, create_dt, upload_dt, filename) VALUES (:id, :file_location, :taken, :uploaded, :filename)",
                            id=session["user_id"], file_location = path, taken = date_taken, uploaded = dt_string, filename = filename)

        # reload index with images once done
        return render_template("upload_files.html")

    # if user reached route via GET
    else:
        return render_template("upload_files.html")


@app.route("/delete_file", methods=["GET", "POST"])
@login_required
def delete_file():

    # if user reached route via POST
    if request.method == "POST":

        # get path of file to delete as given from the button
        path = request.form.get("delete_file_btn")

        # remove file from images database
        db.execute("DELETE FROM images WHERE location = :location", location = path)

        # remove actual file
        os.remove(path)

        # reload the page
        return index()

    # if user reached route via GET
    else:
        return index()


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    # if user reached route via POST
    if request.method == "POST":

        # initialize variables for the new + old password and password confirmation from the form
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # query database for current user's current password
        rows = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])

        # if no old password is submitted, apologize
        if not old_password:
            broadcast("Please provide your old password.")
            return render_template("change_password.html")

        # if no new password is submitted, apologize
        if not new_password:
            broadcast("Please provide a new password.")
            return render_template("change_password.html")

        # if no password confirmation is submitted, apologize
        elif not confirmation:
            broadcast("Please confirm your new password.")
            return render_template("change_password.html")

        # check confirmation password and inputted passwords match
        elif not confirmation == new_password:
            broadcast("Passwords need to match.")
            return render_template("change_password.html")

        # check the old password matches what's in the database
        elif not check_password_hash(rows[0]["hash"], old_password):
            broadcast("Incorrect old password.")
            return render_template("change_password.html")

        else:

            # generate password hash and input the new username and password into the database
            password_hash = generate_password_hash(new_password, "sha256")
            db.execute("UPDATE users SET hash = :newpass WHERE id = :id",  newpass=password_hash, id=session["user_id"])

            # redirect user back to their home page
            return redirect("/")

    # if user reached route via GET
    else:
        return render_template("change_password.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            broadcast("Please provide a username.")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            broadcast("Please provide a password.")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            broadcast("Invalid username and/or password.")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return broadcast(e.name, e.code)

# From flask documentation
# https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


