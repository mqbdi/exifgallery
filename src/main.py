import os

import exifread
from flask import Flask
from flask.templating import render_template


app = Flask(__name__)


class FileImage(object):
    path = None
    date = None
    thumbnail = None
    geospartial = None
    
    def __init__(self):
        pass



def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

def print_exif(filename): 
    # Open image file for reading (binary mode)
    f = open(filename, 'rb')
    # Return Exif tags
    tags = exifread.process_file(f, details=False)
    for tag in tags.keys():
        if tag in ('EXIF DateTimeOriginal', 'JPEGThumbnail', 'Image Model'): #, 'JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            print "file: %s, key: %s, value %s" % (filename, tag, tags[tag])
    # print(" file " + filename + "  tags: " + str(tags))

@app.route("/")
def hello():
    mypath = "/home/mib/Bilder/Kamera/"
    # Run the above function and store its results in a variable.   
    onlyfiles = get_filepaths(mypath)
    # onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for f in onlyfiles:
        print_exif(f)
    
    return render_template('default-template.html')
    # return "Hello World!"

@app.route("/login")
def login():
    return "TODO"

@app.route("/logout")
def logoff():
    return "TODO"

if __name__ == "__main__":
    app.debug = True;
    app.run()