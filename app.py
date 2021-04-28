import os
import job
import time
from flask_dropzone import Dropzone
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file, redirect, url_for

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='default',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
)

dropzone = Dropzone(app)


@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        file_path = os.path.join(app.config['UPLOADED_PATH'], f.filename)
        f.save(file_path)

        oh, lh = job.get_hours(file_path)
        file = job.fill_table(oh, lh)

    return render_template('index.html')


@app.route('/download')
def download():
    return send_file("templates/template_5days_filled.csv", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
