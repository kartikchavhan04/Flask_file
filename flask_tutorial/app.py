from click import edit
from flask import Flask, flash ,render_template,request, url_for,redirect
from form import MyForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key '
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class user(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    profile = db.relationship('profile', backref='user', uselist=False) 

def __repr__(self):
    return f"User('{self.id}','{self.name}', '{self.email}')"

class profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)




@app.route('/')
def index():
    items = ['apple','banana','mango']
    return render_template('index.html',items=items)    

@app.route('/users')
def users():
    users = user.query.order_by(user.id.asc()).all()
    form = MyForm()
    return render_template('users/index.html', users=users , form=form)

@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    form = MyForm()
    if form.validate_on_submit():
        new_user = user(name=form.name.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        new_profile = profile(bio='This is a sample bio', user_id=new_user.id)
        db.session.add(new_profile)
        db.session.commit()


        flash('User created successfully!', 'success')
        return redirect(url_for('users'))
    return render_template('users/create.html', form=form)

@app.route('/users/<int:id>')
def show_user(id):
    user1 = user.query.order_by(user.id.asc()).get(id)
    return render_template('users/show.html', user=user1)

@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    user1 = user.query.order_by(user.id.asc()).get(id)
    form = MyForm(obj=user1)
    if form.validate_on_submit():
        user1.name = form.name.data
        user1.email = form.email.data
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('users'))
    return render_template ('users/edit.html',  form= form, user=user1)

@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    user1 = user.query.get(id)
    db.session.delete(user1)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('users'))

@app.route('/submit',methods =['GET','POST'])
def submit():
    form = MyForm()

    if form.validate_on_submit():

        new_user = user(name=form.name.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()


        flash('Form submitted successfully!')
        return redirect(url_for('submit'))
    else:
        return render_template('from.html', form=form)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)