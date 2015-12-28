
import exifread
import json
import io
import os
import flask
from fractions import Fraction


app = flask.Flask(__name__)

# the file to store and read the image file index
indexfile = "imagefile.json"

# these date tags should be synchronized
DATETAGS = ['EXIF DateTimeOriginal', 'Image DateTime', 'EXIF DateTimeDigitized']


class FileImage(object):
    # full qualified path
    fqpath = None
    # exif creation date
    exifdate = None
    geolocation = None
    exif = None
    
    def __init__(self):
        pass
    
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def get_configuredpaths():
    """
    This function will return all currently configured locations of image folders. 
    This is configured in the file 'imports.properties'. 
    """
    # file_paths = ['/home/mib/Bilder/Kamera/']
    file_paths = ['/home/mib/Bilder/Matthias2Sicherung']
    # TODO load configuration file with import paths 
    return file_paths

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

def _convert_to_degress(value):
    # http://www.sparkgeo.com/blog/mapping-exif-files/
    """Helper function to convert the GPS coordinates stored in the EXIF to degrees in float format"""
    d = float(Fraction(str(value.values[0])))
    m = float(Fraction(str(value.values[1]))) 
    s = float(Fraction(str(value.values[2])))
    return d + (m / 60.0) + (s / 3600.0) 

def print_exif(filename): 
    # Open image file for reading (binary mode)
    f = io.open(filename, 'rb')
    # Return Exif tags
    tags = exifread.process_file(f, details=False)
    for tag in tags.keys():
        if tag in ('EXIF DateTimeOriginal', 'JPEGThumbnail', 'Image Model'):  # , 'JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            print "file: %s, key: %s, value %s" % (filename, tag, tags[tag])
    # print(" file " + filename + "  tags: " + str(tags))

@app.route("/")
def hello():
    mypath = get_configuredpaths()
    # Run the above function and store its results in a variable.   
    onlyfiles = get_filepaths(mypath)
    # onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for f in onlyfiles:
        print_exif(f)
    
    return flask.templating.render_template('default-template.html')
    # return "Hello World!"

@app.route("/build")
def build():
    imagefiles = []
    paths = get_configuredpaths()
    for path in paths:
        files = get_filepaths(path)
        for filename in files:
            fp = io.open(filename, 'rb')
            exiftags = exifread.process_file(fp, details=False)
            # print (filename + "\t" + str(exiftags.keys() ))
            meta = FileImage()
            meta.fqpath = filename

#             if exiftags.has_key('EXIF DateTimeOriginal'):
#                 print(filename + " EXIF DateTimeOriginal " + exiftags.get('EXIF DateTimeOriginal').values )
#             if exiftags.has_key('Image DateTime'):
#                 print(filename + " Image DateTime " + exiftags.get('Image DateTime').values )
            if exiftags.has_key('EXIF DateTimeDigitized'): 
                print(filename + " EXIF DateTimeDigitized " + exiftags.get('EXIF DateTimeDigitized').values )
                meta.exifdate = exiftags.get('EXIF DateTimeDigitized').values
#            'GPS GPSLatitudeRef', 'GPS GPSLatitude'
#            'GPS GPSLongitude', 'GPS GPSLongitudeRef', 'Image GPSInfo', 
            
            lat = None
            lon = None
            
            if exiftags.has_key('GPS GPSLatitude'): 
                lat = _convert_to_degress(exiftags.get('GPS GPSLatitude'))
                latref = exiftags.get('GPS GPSLatitudeRef').values
                if latref != "N":
                    lat = 0 - lat

                print(filename + ' GPS GPSLatitude ' + str(exiftags.get('GPS GPSLatitude').values) + str(exiftags.get('GPS GPSLatitudeRef').values) )

            if exiftags.has_key('GPS GPSLongitude'): 
                lon = _convert_to_degress(exiftags.get('GPS GPSLongitude'))
                lonref = exiftags.get('GPS GPSLongitudeRef').values
                if lonref != 'E':
                    lon = 0 - lon

                print(filename + ' GPS GPSLongitude ' + str(exiftags.get('GPS GPSLongitude').values) + str(exiftags.get('GPS GPSLongitudeRef').values) )

            if lat and lon:
                meta.geolocation = str(lat) + ';' + str(lon)
#             if exiftags.has_key('Image GPSInfo'): 
#                 print(filename + ' Image GPSInfo ' + str(exiftags.get('Image GPSInfo').values) )

            
            #print(filename + " " + exiftags['JPEGThumbnail'])
            # meta.thumbnail = exiftags['JPEGThumbnail']
            imagefiles.append(meta)
    jsonfile = io.open(indexfile, 'w', encoding='utf-8')
    # print json.dumps([ i.__dict__  imagefiles ])
    jsonfile.write(unicode(json.dumps( [i.__dict__ for i in imagefiles], ensure_ascii=False, indent=2)))
    # json.dump(unicode( imagefiles ), jsonfile)
    jsonfile.flush()
    jsonfile.close()
    
    print len(imagefiles)
    return flask.templating.render_template('default-template.html')

@app.route("/login")
def login():
    return "TODO"

@app.route("/logout")
def logoff():
    return "TODO"

if __name__ == "__main__":
    app.debug = True;
    app.run()
