from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "welcome to simple interest calculator"

@app.route('/calculator/<float:principal>/<float:rate>/<int:time>')
def index(principal, rate, time):
    simple_interest = (principal * rate * time) / 100
    return f"The simple interest for principal {principal}, rate {rate}%, and time {time} years is = {simple_interest}"

@app.route('/calculate', methods=['POST'])
def calculate():
    principal = float(request.form['principal'])
    rate = float(request.form['rate'])
    time = float(request.form['time'])

    simple_interest = (principal * rate * time) / 100

    return f"The simple interest for principal {principal}, rate {rate}%, and time {time} years is = {simple_interest}"

if __name__ == "__main__":
    app.run(debug=True) 


