from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
from forms import LoginForm, RegForm

from flask_sqlalchemy import SQLAlchemy

import os



app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Set the login view
app.config['SECRET_KEY'] = '32659db159db1a52cd39b981b2f56a22'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///init_db.sql'
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/member-page')
@login_required
def member():
    return render_template('members.html')



UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Some logic to determine if the user is authenticated
    return render_template('index.html', current_user=current_user)

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



@app.route('/submit-claim', methods=['GET', 'POST'])
@login_required
def submit_claim():
    # Your form processing logic here
    return render_template('submit_claim.html')

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # or any other page you consider as home
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('submit_claim'))  # Redirect to submit claim form
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    return render_template('login.html', form=form)


    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Redirect to the home page if already logged in
    form = RegForm()  # Create an instance of the registration form
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)  # Create a new user object
        user.set_password(form.password.data)  # Set the password for the new user
        db.session.add(user)  # Add the user to the database session
        db.session.commit()  # Commit the changes to the database
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))  # Redirect to the login page after successful registration
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/logout')
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('index'))  # Redirect to the home page after logout


if __name__ == '__main__':
    app.run(debug=True)
 
