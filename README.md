# Flask

Flask is a lightweight and flexible Python web framework used to develop web applications and REST APIs.

## Installation

```bash
pip install flask
```

## Basic Flask Application

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)
```

## Run Flask Application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000/
```

## Main Concepts

* **Application** – Creates the Flask application.
* **Route** – Connects a URL with a Python function.
* **View Function** – Contains the logic for a route.
* **Request** – Receives data from the client.
* **Response** – Sends data back to the client.
* **Template** – Used to create dynamic HTML pages.
* **Static Files** – CSS, JavaScript, and images.
* **Session** – Stores user information between requests.

## HTTP Methods

```text
GET     → Read data
POST    → Create data
PUT     → Update data
DELETE  → Delete data
```

## Flask Structure

```text
flask_app/
│
├── app.py
├── templates/
│   └── index.html
└── static/
    ├── css/
    ├── js/
    └── images/
```

## Database

Flask can work with databases such as MySQL, PostgreSQL, and SQLite.

For MySQL with SQLAlchemy:

```bash
pip install flask-sqlalchemy pymysql
```

## Flask Flow

```text
Browser
   ↓
Request
   ↓
Flask Route
   ↓
View Function
   ↓
Business Logic
   ↓
Database
   ↓
Response
   ↓
Browser
```

## Features

* Lightweight framework
* Easy routing
* Jinja2 template support
* REST API development
* Database integration
* Authentication support
* Large extension ecosystem

## Author

**Kartik Chavhan**
