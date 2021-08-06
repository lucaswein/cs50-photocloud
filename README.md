# About Photocloud

Photocloud is a minimalistic yet effetive web app for backing up and viewing images. Users can upload images to their dashboard. Here, they're organized based on when the pictures were taken (or if not, when they were uploaded), and users can delete them as they wish.

## Languages

Photocloud uses:
- Python (Flask)
- MySQL
- HTML
- CSS
- Javascript
- JQuery

# Installation

1. Zip and install all necessary files uploaded.
2. Extract the zipped file.
3. Ensure python 3.9.1 is installed.
4. Ensure all necessary python libraries (listed in the [requirements](requirements.md)) are installed.
5. Open a terminal window in the unzipped folder.
6. Run `flask run` to start the application.
7. Open the link provided to get to the photocloud application.

# Getting Started

## Making an Account

Upon the first boot og photocloud, all databases will be empty. Although you'll be prompted at a log in screen, no accounts exist that you can log in with. You'll have to click the **Register** button located furthest to the left in the navbar in order to register a new account. Here, you'll have to come up with a username and password, and confirm the password you enter. You might want to right this down as to not get locked out of your account. Once you've entered your username, password and confirmed your password, click **Register**.

## Logging in

Now, you'll be redirected to the log in page you were at before. Enter the username and password you just came up with, and click **Log In**.

## Uploading Images

Once you're logged in, you'll be redirected to a mostly blank page. This is where your images would normally load, but you haven't uploaded any yet. You may have noticed that your navbar has changed since you logged in. Now there's an option to go back home (where you are right now), upload images, and a dropdown menu for your account that will let you change your password and log out. Right now, we want to upload some images. Click on the **Upload** link at the navbar.

You'll be redirected to a page with two buttons: one will let you choose the files you want to upload, and the other will upload the files you've chosen. As stated above both buttons, the only file types you'll be able to upload include `.png`, `.jpg` and `.gif`. 
