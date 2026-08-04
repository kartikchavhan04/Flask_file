from flask import Flask, request, jsonify, send_from_directory
from wtforms import Field
from pydantic import BaseModel, ValidationError

app = Flask(__name__)

class User(BaseModel):
    name : str = Field(..., min_length=2, max_length=100)
    email : str = Field(..., regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    number : int = Field(..., ge=0, le=100)
    address : str = Field(..., min_length=5, max_length=200)

@app.route('/validate_user', methods=['POST'])
def validate_user():
    try:
        user = request.get_json()
        user = User(**user)

        return jsonify({
            'status': 'success',
            'massage': 'User is valid',
            'data': user.model_dump()
        }), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400

    return jsonify({
        'status': 'error',
        'massage': 'validation error',
        'data': e.errors()
    }), 400

if __name__ == "__main__":
    app.run(debug=True)