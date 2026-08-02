from flask import Flask, session

app = Flask(__name__)

# Session sathi secret key compulsory aahe
app.secret_key = "my_secret_key"


# Login
@app.route("/login")
def login():

    session["username"] = "Kartik Chavhan"

    return "Login Successful"


# Profile
@app.route("/profile")
def profile():

    if "username" in session:
        return f"Welcome {session['username']}"

    return "Please Login First"


# Logout
@app.route("/logout")
def logout():

    session.pop("username", None)

    return "Logout Successful"


if __name__ == "__main__":
    app.run(debug=True)