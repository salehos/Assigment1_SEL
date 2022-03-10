import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.middleware.shared_data import SharedDataMiddleware
from pdf_merger import PDFMergerUtil
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ""


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if ('first_file' not in request.files) or ('second_file' not in request.files) :
            flash('No file part')
            return redirect(request.url)
        first_file = request.files['first_file']
        second_file = request.files['second_file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if first_file.filename == '' or second_file.filename =='':
            flash('No selected file')
            return redirect(request.url)
        if first_file and allowed_file(first_file.filename) and (second_file and allowed_file(second_file.filename)):
            first_filename = secure_filename(first_file.filename)
            second_filename = secure_filename(second_file.filename)
            first_file.save(os.path.join(app.config['UPLOAD_FOLDER'], first_filename))
            second_file.save(os.path.join(app.config['UPLOAD_FOLDER'], second_filename))
            pdfMergerObj = PDFMergerUtil.merge([first_filename, second_filename],str(first_filename).replace(".pdf","")+str(second_filename))
            return redirect(url_for('uploaded_file',
                                    filename=str(first_filename).replace(".pdf","")+str(second_filename).replace(".pdf","")+".pdf"))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=first_file>
      <br>
      <input type=file name=second_file>
      <br>
      <input type=submit value=Upload>
    </form>
    '''
		

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})

if __name__ == '__main__':
   app.run(debug = True)