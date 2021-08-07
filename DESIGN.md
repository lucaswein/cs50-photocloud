# Photocloud Structure

In general, Photocloud's structure is similar to that of any other Python Flask web application, and is a heavily modified version of CS50's **finance**.

# Front End

The `templates` and `static` folders make up everything in the front end. 

## 'templates'

### layout.html
*inside templates*

'Templates' contains html files for each page of the website. All of the html files (besides `layout.html`) extend [layout.html](templates/layout.html). This html file contains a header that imports jQuery, bootstrap and iconify scripts, as well as the favicon, local styles, and bootstrap styles. 

`layout.html` also adds "PHOTOCLOUD -" to the title of each page, uses flask to display different navbars depending on if the user is logged in or not, flashes error, warning or info messages at the top of the screen, and adds a footer to each page.

This page is primarily html, but loads and uses javascript and css.
The page also uses Python Flask to load anything from backend.

### scripts and styles used

- `jQuery` script is used for bootstrap and lightboxes in the ekkoLightbox script (used and explained later)
- `bootstrap` scripts and styles are used to structure everything on the front end (forms, buttons, navbar, etc.)
- `iconify` script is used to load iconify's svg files (in this case the trash can as the delete button)

### Other html files

Every other html file extends `layout.html`, importing all scripts and styles mentioned above. Most are simple html forms that send information to the Python Flask backend.

### 'index.html'
*not to be confused with `layout.html`*

`index.html` is special in that it loads in scripts for ekkoLightbox. This is a script that extends bootstrap and allows configuration of lightboxes (when an image becomes full screen when clicked on). 

This file is also rendered from the backend with information about all the user's images. It runs through a dictionary of this information and loads each image, as well as the image name. Each image is also loaded with a delete button, which is a form that loads a backend Python Flask function. This button returns the path of the images to remove.

## 'static'

The static folder contains anything a user would need access to load, such as images and favicons. As such, uploaded images, a script for lightboxes, custom styles and the icon and favicon are all readily available.

# Back End

The back end of photocloud is primarily coded in Python Flask, but uses a MySQL database to keep record of each image.

## MySQL structure

`photocloud.db` is an sqlite3 database that remembers all the information about users and their images. 

The database schematic can be broken up into two main tables: the users table, and the images table.
```
CREATE TABLE users (id INTEGER, username TEXT NOT NULL, hash TEXT NOT NULL, PRIMARY KEY(id));
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE images (user_id INTEGAR, location TEXT NOT NULL, upload_dt TEXT, create_dt TEXT, filename TEXT NOT NULL);
```

Inside the `user` table, a user id is given and stores to each row of users, as well as their username and hashed password (stored as hash). Every image is documented in the `images` table with the `user_id` it was uploaded under, file location, time uploaded and created, and name of file. Information for all of this is inputted through the Python Flask backend.

## 'helpers.py'

This python file has functions used throughout `application.py` (the main file).

### get_date_taken

This function gets the date a picture was taken. It uses the PIL library to look through the metadata of an image and get the date it was taken. If it's not there, it will return with 'None'.

### broadcast

Broadcast flashes messages to users. This function is used instead of directly flashing to enable debugging.

### login_required

Require uses to log in before accessing certain pages.

## 'application.py'

This is the main backend file that brings together everything from rendering the html to modifying the databases.

At the start of the file is every library imported. As a quick overview:

- `os` allows modifying files, making files, finding file paths
- `SQL from cs50` allows making MySQL queries from Python
- anything relating to `flask` allows rendering pages and stringing together the back and front end
- assorted imports from `werkzeug` allow for running the http server, hashing user passwords, correctly getting filenames
- `PIL` finds metadata of images, used when finding when pictures were taken
- `datetime` allows converting time formats and finding the current time
- `logging` allows debugging in the Python console
- anything from `helpers` includes the functions mentioned for `helpers.py`

Then, flask is configured to upload files and disable cache, and the database file is initialized.

### index

`index()` gets all the images from the current user, sorts them by either the time they were taken or the time they were uploaded (not all images include the time they were taken), and sends them off as a dictionary to render as `index.html`.

### logout

`logout()` allows users to logout by forgetting the user's id, and redirects the user to the login page. 

### register

This function grabs the information inputted by the form on `register.html`, such as the username, password and password confirmation, and runs tests to make sure everything is eligble to go into the database (ex. if the username, password and confirmation all exist, that the password and confirmation match each other)

Then, a new user is added to the databse; the inputted username and password are recorded.

### upload_files

This function gets all the files the user uploaded from the `upload_files.html` form. It runs through each file uploaded, makes sure they have the right extensions, and tests if any are duplicates. If they are, a number is added to however many duplicates there already are. (Ex. if `image.png` is uploaded 3 times, the files will become `image1.png`, `image2.png`, and `image3.png`.

Information about the files, such as the user id who uploaded them, time uploaded, taken, file path and file name are all stored in the images database. And, finally, the images themselves are stored in the uploads folder.

Once all of this is done, `upload_files.html` is reloaded.

### delete_file

This function takes input from the trash can delete button in `index.html`, and removes the image from the uploads folder and images database. Once done, it reloads the `index()` function as to reload the page with data.

### change_password

This function takes input from the `change_password.html` input form. Similar to `register()`, it makes sure the user has entered the correct old password, and that they confirm their new password. If this is all true, it will update the database with the user's new password.

### login

Takes input from the `login.html` form. If the username inputted exists and the password matches, it'll log the user in.

### allowed_file

Function used in uploading files, makes sure whatever files it sees have allowed extensions (`.png`, `.jpg`, `.gif`)
