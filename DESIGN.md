# Photocloud Structure

In general, Photocloud's structure is similar to that of any other Python Flask web application.

# Front End

The 'templates' and 'static' folders make up everything in the front end. 

## 'templates'

### layout.html
*inside templates*

'Templates' contains html files for each page of the website. All of the html files (besides layout.html) extend [layout.html](templates/layout.html). This html file contains a header that imports jQuery, bootstrap and iconify scripts, as well as the favicon, local styles, and bootstrap styles. 

layout.html also adds "PHOTOCLOUD -" to the title of each page, uses flask to display different navbars depending on if the user is logged in or not, flashes error, warning or info messages at the top of the screen, and adds a footer to each page.

This page is primarily html, but loads and uses javascript and css.
The page also uses Python Flask to load anything from backend.

### scripts and styles used

- jQuery is used for bootstrap and lightboxes in the ekkoLightbox script (used and explained later)
- bootstrap scripts and styles are used to structure everything on the front end (forms, buttons, navbar, etc.)
- iconify is used to load iconify's svg files (in this case the trash can as the delete button)

### Other html files

Every other html file extends layout.html, importing all scripts and styles mentioned above. Most are simple html forms that send information to the Python Flask backend.

### index.html
*not to be confused with layout.html*

index.html is special in that it loads in scripts for ekkoLightbox. This is a script that extends bootstrap and allows configuration of lightboxes (when an image becomes full screen when clicked on). 

This file is also rendered from the backend with information about all the user's images. It runs through a dictionary of this information and loads each image, as well as the image name. Each image is also loaded with a delete button, which is a form that loads a backend Python Flask function. This button returns the path of the images to remove.

## 'static'

The static folder contains anything a user would need access to load, such as images and favicons. As such, uploaded images, a script for lightboxes, custom styles and the icon and favicon are all readily available.

# Back end



