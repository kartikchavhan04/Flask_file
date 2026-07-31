from click import edit
from flask import Flask, flash ,render_template,request, url_for,redirect
from form import MyForm
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key '
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class user(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>',{self.email}

@app.route('/')
def index():
    items = ['apple','banana','mango']
    return render_template('index.html', items=items)

@app.route('/users')
def users():
    users = user.query.all()
    return render_template('users/index.html', users=users)

@app.route('/users/<int:user_id>/edit')
def edit(user_id):
    user1 = user.query.get(user_id)
    form = MyForm(obj=user1)
    return render_template ('users/edit.html',  form= form, users=users)

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


if __name__ == "__main__":
    app.run(debug=True)