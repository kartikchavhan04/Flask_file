from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)

student = {

    "id": 101,
    "name": "Kartik",
    "age": 22,
    "city": "Pune"
}

@app.route("/student", methods=["DELETE"])
def delete_student():
    student.clear()
    return jsonify({"message": "Student deleted successfully"})

@app.route("/student", methods=["PATCH"])
def update_student():

    data = request.json

    student.update(data)

    return jsonify(student)

@app.route("/student", methods=["PUT"])
def replace_student():
    data = request.json
    student.clear()
    student.update(data)
    return jsonify(student)

@app.route('/student', methods=['POST'])
def create_student():
    data = request.get_json()  

    name = data['name'] 
    age = data['age'] 


    return jsonify(f"welcome unemployed {name} your age is {age} ")

if __name__ == '__main__':
    app.run(debug=True)
