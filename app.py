# server app
from flask import Flask, render_template, request, session, url_for, redirect
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os

# Init & Config
app = Flask(__name__)
dropzone = Dropzone(app)
# Session key
app.config['SECRET_KEY'] = 'secret_key'

# Dropzone settings

app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
# Upload->(Redirect)->results.html(@app.route(results))
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'

# Upload settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'

# An “upload set” is a single collection of files. You just declare them in the code:
photos = UploadSet('photos', IMAGES)
# It will go through all the upload sets, 
# get their configuration, and store the configuration on the app
configure_uploads(app, photos)
patch_request_class(app) # Max file size



# Routes for app
@app.route('/', methods=['GET', 'POST'])
def index():

    #Sessions
    if "file_urls" not in session:
        session['file_urls'] = []

    #List for images
    file_urls = session['file_urls']

    if request.method == 'POST':
        file_obj = request.files
        # Dropzone allowed for multiple uploads
        for f in file_obj:
            file = request.files.get(f)
            filename = photos.save(file, name=file.filename)
            file_urls.append(photos.url(filename))
        session['file_urls'] = file_urls
        return "uploading..."
    return render_template('index.html')
@app.route('/results')
def results():
    #If no images to show, redirect to home
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))
    file_urls = session['file_urls']
    session.pop('file_urls', None)
    return render_template('results.html', file_urls=file_urls)
# Extra
@app.route('/about')
def about():
    return render_template('about.html')