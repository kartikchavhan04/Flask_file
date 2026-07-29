from flask import Flask, request

app = Flask(__name__)


@app.route('/add/<int:number1>/<int:number2>')
def add(number1, number2):
    result = number1 + number2
    return f"The sum of {number1} and {number2} is: {result}"


@app.route('/sub/<int:number1>/<int:number2>')
def sub(number1, number2):
    result = number1 - number2
    return f"The difference between {number1} and {number2} is: {result}"


@app.route('/mul/<int:number1>/<int:number2>')
def mul(number1, number2):
    result = number1 * number2
    return f"The product of {number1} and {number2} is: {result}"


@app.route('/div/<int:number1>/<int:number2>')
def div(number1, number2):
    if number2 == 0:
        return "Error: Division by zero is not allowed."

    result = number1 / number2
    return f"The quotient is: {result}"


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():

    if request.method == 'POST':

        number1 = int(request.form['number1'])
        number2 = int(request.form['number2'])
        operation = request.form['operation']

        if operation == 'add':
            result = number1 + number2

        elif operation == 'sub':
            result = number1 - number2

        elif operation == 'mul':
            result = number1 * number2

        elif operation == 'div':
            if number2 == 0:
                return "Division by zero is not allowed."

            result = number1 / number2

        else:
            return "Invalid Operation"

        return f"Answer = {result}"

    return """
    Please send a POST request.

    Body (x-www-form-urlencoded)

    number1 = 10
    number2 = 20
    operation = add
    """


if __name__ == "__main__":
    app.run(debug=True)