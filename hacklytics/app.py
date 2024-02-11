from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
from .forms import LoginForm, RegForm

from flask_sqlalchemy import SQLAlchemy

from .llm.model import model_function
from .llm.prompt import get_issues_and_fixes
from .llm.prompt_response import PromptResponse

import os



app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Set the login view
app.config['SECRET_KEY'] = '32659db159db1a52cd39b981b2f56a22'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///init_db.sql'
db = SQLAlchemy(app)



class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    policy_number = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    images = db.relationship('Image', backref='claim', lazy=True)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    claim_id = db.Column(db.Integer, db.ForeignKey('claim.id'), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Place the db.create_all() call here, after model definitions
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/member-page')
@login_required
def member():
    # Retrieve claims for the current user
    user_claims = Claim.query.filter_by(user_id=current_user.id).all()
    # Pass the claims to the template
    return render_template('members.html', claims=user_claims)



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
    if request.method == 'POST':
        print(request.form)  # Log form data
        print(request.files)  # Log file data
        policy_number = request.form['policyNumber']
        files = request.files.getlist('images')
        description = request.form['description']
        

        new_claim = Claim(policy_number=policy_number, description=description, user_id=current_user.id)
        db.session.add(new_claim)

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                new_image = Image(filename=filename, claim=new_claim)
                db.session.add(new_image)
        # After saving the claim and its images...
        db.session.commit()
        flash('Claim submitted successfully!', 'success')

        # Redirect to the view_claim route, passing the new claim's ID
        return redirect(url_for('view_claim', claim_id=new_claim.id))
    
    # If it's a GET request, just render the submit claim form
    return render_template('submit_claim.html')


@app.route('/view-claim/<int:claim_id>')
@login_required
def view_claim(claim_id):
    # new comment
    claim = Claim.query.get_or_404(claim_id)
    if claim.user_id != current_user.id:
        flash('Unauthorized to view this claim.', 'danger')
        return redirect(url_for('index'))

    images = Image.query.filter_by(claim_id=claim.id).all()
    filenames = [image.filename for image in images]
    return render_template('viewer.html', claim=claim, filenames=filenames)





    
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
        return redirect(url_for('index'))
    form = RegForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # Hash and store the password
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/logout')
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('index'))  # Redirect to the home page after logout


if __name__ == '__main__':
    app.run(debug=True)