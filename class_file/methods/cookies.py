from flask import Flask, request, make_response

app = Flask(__name__)

# Cookie Set
@app.route("/set-cookie")
def set_cookie():

    response = make_response("Cookie Saved Successfully")

    response.set_cookie("username", "Kartik")

    return response


# Cookie Read
@app.route("/get-cookie")
def get_cookie():

    username = request.cookies.get("username")

    return f"Username = {username}"


# Cookie Delete
@app.route("/delete-cookie")
def delete_cookie():

    response = make_response("Cookie Deleted Successfully")

    response.delete_cookie("username")

    return response


if __name__ == "__main__":
    app.run(debug=True)