from click import edit
from flask import Flask, flash ,render_template,request, url_for,redirect
from numpy import delete
from form import MyForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key '
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) # Set the upload folder path
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}# Set the upload folder path['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed file extensions  

db = SQLAlchemy(app)

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    file_name = db.Column(db.String(200), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship('profile', backref='blog', lazy=True)
    def __repr__(self):
        return f"Blog('{self.id}', '{self.title}', '{self.date_posted}', '{self.content}')"


def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )
@app.route('/blogs')
def blogs():
    blog1 = Blog.query.order_by(Blog.id.asc()).all()
    return render_template('blogs/index.html', blogs=blog1)

@app.route('/blogs/new', methods=['GET', 'POST'])
def create_blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file = request.files['image_file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        else:
            filename = 'default.jpg'
            
        new_blog = Blog (title=title, content=content, file_name=filename)
        db.session.add(new_blog)
        db.session.commit()

        new_profile = profile(bio='This is a sample bio', user_id=new_blog.id)
        db.session.add(new_profile)
        db.session.commit()
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('blogs'))
    
    return render_template('blogs/create.html')


@app.route('/blogs/<int:id>/delete', methods=['POST'])
def delete_blog(id):
    blog1 = Blog.query.get(id)
    db.session.delete(blog1)
    db.session.commit()
    flash('Blog post deleted successfully!', 'success')
    return redirect(url_for('blogs'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)