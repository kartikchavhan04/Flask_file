from flask import Flask, flash ,render_template,request, url_for,redirect

app = Flask(__name__)

@app.route('/')
def index():
    return "welcome to calculator app"

@app.route('/add/<int:number1>/<int:number2>')
def add(number1, number2):
    result = number1 + number2
    return (f"The sum of {number1} and {number2} is: {result}")

@app.route('/sub/<int:number1>/<int:number2>')
def sub(number1, number2):
    result = number1 - number2
    return (f"The difference between {number1} and {number2} is: {result}")

@app.route('/mul/<int:number1>/<int:number2>')
def mul(number1, number2):
    result = number1 * number2
    return (f"The product of {number1} and {number2} is: {result}")

@app.route('/div/<int:number1>/<int:number2>')
def div(number1, number2):
    if number2 == 0:
        return "Error: Division by zero is not allowed."
    result = number1 / number2
    return (f"The quotient of {number1} divided by {number2} is: {result}")

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        number1 = int(request.form['number1'])
        number2 = int(request.form['number2'])
        operation = request.form['operation']

        if operation == 'add':
            result = number1 + number2
            return f"answer: {result}"
        elif operation == 'sub':
            result = number1 - number2
            return f"answer: {result}"
        elif operation == 'mul':
            result = number1 * number2
            return f"answer: {result}"
        elif operation == 'div':
            if number2 == 0:
                return "Error: Division by zero is not allowed."
            result = number1 / number2
            return f"answer: {result}"
    else:
        return "please send a post request with number1, number2, and operation in the form data."

if __name__ == "__main__":
    app.run(debug=True)