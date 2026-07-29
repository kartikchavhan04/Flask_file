from flask import Flask, flash ,render_template,request, url_for,redirect
from form import MyForm
app = Flask(__name__)
app .config['SECRET_KEY'] = 'your_secret_key'   

@app.route('/')
def index():
    items = ['apple','banana','mango']
    return render_template('index.html', items=items)

@app.route('/submit',methods =['GET','POST'])
def submit():
    form = MyForm()

    if form.validate_on_submit():
        flash('Form submitted successfully!')
        return redirect(url_for('submit'))
    else:
        return render_template('from.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)