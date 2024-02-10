from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')  # If you decide to add a home route distinct from index
def home():
    return render_template('index.html')  # Assuming you have a home.html template

@app.route('/claims')
def claims():
    return render_template('claims.html')  # Assuming you have a claims.html template

@app.route('/contact')
def contact():
    return render_template('contact.html')  # Assuming you have a contact.html template


@app.route('/viewer')
def viewer():
    return render_template('viewer.html')

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/submit-claim', methods=['POST'])
def submit_claim():
    if request.method == 'POST':
        # Form processing and file upload handling code remains unchanged
        return redirect(url_for('viewer'))
    
    

if __name__ == '__main__':
    app.run(debug=True)
