from click import edit
from flask import Flask, flash ,render_template,request, url_for,redirect
from form import RegisterForm,LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,LoginManager,login_user,current_user,login_required,logout_user
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key '
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager(app)
login_manager.login_view = "login"


db = SQLAlchemy(app)


class user(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # confirm_password = db.Column(db.String(100),)


@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
   
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = user(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('User registered successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html' , form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = user.query.filter_by(email=form.email.data).first()
        if users and check_password_hash(users.password,form.password.data):
            login_user(users)
            flash("login Successful")
            return redirect(url_for('dashboard'))
        else:
            flash("login failed..Check email Or Password")
    return render_template("auth/login.html",form=form)

    
@app.route('/dashboard')
@login_required 
def dashboard():
    return render_template("dashboard.html")

@app.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)