from flask import Flask ,request,render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hello , world"

@app.route('/user/<username>/<age>')
def show_user_profile(username,age):
    return render_template('user.html',username=username,age=age)

@app.route('/post/<int:post_id>',methods=['GET'])
def show_post(post_id):
    return 'post %d' %post_id

@app.route('/submit',methods =['GET','POST'])
def submit_data():
    if request.method== 'POST':
        name = request.form['name']
        age = request.form['age']
        return 'Data submitted successfully! Name: {}, Age: {}'.format(name, age)
    else:
        return render_template('from.html')

@app.route('/profile')
def profile():
    
    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=True)