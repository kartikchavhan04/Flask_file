from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def home():
    li1={"name":'kartik',"age":23}

    return render_template('home.html' ,li1=li1)
@app.route('/about')
def about():
    return "this is about page "


@app.route('/<name>')
def user(name):
    return f'Welcome {name}'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)