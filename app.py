#!/usr/bin/env python3
# coding: utf-8

import os
from flask import Flask, request, redirect, url_for, render_template
import gpxdf
import hashlib

UPLOAD_FOLDER = os.path.abspath('./uploads')
ALLOWED_EXTENSIONS = set(['gpx'])

app = Flask(__name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = hashlib.md5(file.filename.encode()).hexdigest()
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
        else:
            return render_template('shimanami.html')
    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    df = gpxdf.read_gpx(os.path.join(UPLOAD_FOLDER, filename))
    gpxdf.to_html_map(df, './templates/map.html', zoom_start=8)
    os.remove(os.path.join(UPLOAD_FOLDER, filename))
    return render_template('map.html')


if __name__ == '__main__':
    app.run()
