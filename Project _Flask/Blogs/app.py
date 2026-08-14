from flask import Flask , render_template, request,redirect,flash,url_for

app = Flask(__name__)
app.secret_key = "my-secret-key"

@app.route("/feedback", methods = ["POST","GET"])
def feedback ():
    if request.method == "POST":
        name = request.form.get("username")
        message = request.form.get("message")
        return render_template("thankyou.html",user=name,message=message)
    return render_template ("feedback.html")

@app.route("/", methods = ["POST","GET"])
def form():
    if request.method == "POST":
        name = request.form.get("name")
        if not name :
            flash ("Name cannot be empty")
            return redirect(url_for("form"))
        flash (f"Thanks {name}, your feedback was saved")
        return redirect(url_for("thankyou"))
    return render_template("feedback.html")
        
@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

@app.route("/register", methods = ["POST","GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        # Validation
        if not username or not email or not password or not confirm_password:
            flash("All fields are required!", "error")
            return redirect(url_for("register"))
        
        if len(password) < 6:
            flash("Password must be at least 6 characters long!", "error")
            return redirect(url_for("register"))
        
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("register"))
        
        # Registration success
        flash(f"Welcome {username}! Registration successful!", "success")
        return render_template("register_success.html", username=username, email=email)
    
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)