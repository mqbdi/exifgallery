# exifgallery

## Motivation

On my search for a suitable image gallery for my local own NAS, I found nothing usable. 

## What it should be!

The vision on ExifGallery is an image viewer based on the EXIF meta data in the header of self made photos. The vision is a viewer that uses local stored file, scan their EXIF and present some useful views on it. File handling could be made by ownCloud, sftp or smb. 

I plan to use the following technologies / libraries
* Python Flask http://flask.pocoo.org to embed this application into a Lighttpd
** Flask based on Werkzeug Jinja2 itsdangerous MarkupSafe
* Using WSGI standard to build applications. 
* Bootstrap CSS and Javascript for web-based views, responsive and compatible for many browsers (unlike Internet Explorer until now)
* JQuery for a living web-application. 

## What it NOT will be! 

* It is not intend to be a web-based upload orgy. 
* It is not intend to be a image file handler. 
* It is not intend to be a directoy image file listing. 

# Developers Information

While developing this application, I use a virtualenv and installed (using pip)
* exifread https://pypi.python.org/pypi/ExifRead
* Flask http://flask.pocoo.org/
