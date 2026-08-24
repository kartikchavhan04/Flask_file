from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Bharat123@localhost/college"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class Task(db.Model):

    __tablename__ = "task"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    status = db.Column(
        db.String(50),
        nullable=False
    )

    priority = db.Column(
        db.String(50),
        nullable=False
    )

    due_date = db.Column(
        db.Date,
        nullable=True
    )

@app.route("/task", methods=["POST"])
def create_task():

    data = request.get_json()

    task = Task(
        title=data["title"],
        description=data("description"),
        status=data["status"],
        priority=data["priority"],
        due_date=(
            datetime.strptime(
                data["due_date"],
                "%Y-%m-%d"
            ).date()
            if data("due_date")
            else None
        )
    )

    db.session.add(task)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Task created successfully",
        "data": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_date": (
                task.due_date.isoformat()
                if task.due_date
                else None
            )
        }
    }), 201

@app.route("/task", methods=["GET"])
def get_all_tasks():

    tasks = Task.query.all()

    task_list = []

    for task in tasks:

        task_list.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_date": (
                task.due_date.isoformat()
                if task.due_date
                else None
            )
        })

    return jsonify({
        "success": True,
        "count": len(task_list),
        "data": task_list
    }), 200

@app.route("/task/<int:task_id>", methods=["PUT"])
def update_task(task_id):

    task = Task.query.get(task_id)

    if not task:

        return jsonify({
            "success": False,
            "message": "Task not found"
        }), 404

    data = request.get_json()

    task.title = data["title"]

    task.description = data.get(
        "description"
    )

    task.status = data["status"]

    task.priority = data["priority"]

    if data.get("due_date"):

        task.due_date = datetime.strptime(
            data["due_date"],
            "%Y-%m-%d"
        ).date()

    else:

        task.due_date = None

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Task updated successfully",
        "data": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_date": (
                task.due_date.isoformat()
                if task.due_date
                else None
            )
        }
    }), 200


@app.route("/task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    task = Task.query.get(task_id)

    if not task:

        return jsonify({
            "success": False,
            "message": "Task not found"
        }), 404

    db.session.delete(task)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Task deleted successfully"
    }), 200


with app.app_context():

    db.create_all()


if __name__ == "__main__":

    app.run(debug=True)