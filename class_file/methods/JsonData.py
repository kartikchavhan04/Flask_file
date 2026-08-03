from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/student", methods=["POST"])
def student_data():
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    grade = data.get("grade")

    # Process the student data as needed
    # For example, you can save it to a database or perform any other operations

    return jsonify({
                    "name": name,
                    "age": age,
                    "grade": grade
                    })

if __name__ == '__main__':
    app.run(debug=True)