from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/interest/<int:principal>/<int:rate>/<int:time>')
def index(principal, rate, time):
    result = principal * (1 + rate) ** time
    # total = result - principal
    return f"The compound interest for principal {principal}, rate {rate}%, and time {time} years is = {result}"

@app.route('/interest', methods=['POST'])
def calculate_interest():
    principal = float(request.form['principal'])
    rate = float(request.form['rate'])
    time = int(request.form['time'])
    result = principal * (1 + rate/100) ** time
    total = result - principal
    return f"The compound interest for principal {principal}, rate {rate}%, and time {time} years is = {total}"

if __name__ == "__main__":
    app.run(debug=True)