from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from app import db
from app.models import Task


tasks_bp = Blueprint(
    "tasks",
    __name__,
    url_prefix="/tasks"
)


# =========================================================
# TASK LIST
# =========================================================

@tasks_bp.route("/")
def task_list():

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    tasks = Task.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Task.id.asc()
    ).all()

    return render_template(
        "tasks.html",
        tasks=tasks
    )


# =========================================================
# ADD TASK
# =========================================================

@tasks_bp.route("/add", methods=["POST"])
def add_task():

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    title = request.form.get(
        "title",
        ""
    ).strip()

    if not title:

        flash(
            "Please enter a task.",
            "error"
        )

        return redirect(
            url_for("tasks.task_list")
        )

    task = Task(
        title=title,
        user_id=session["user_id"],
        status="pending"
    )

    db.session.add(task)
    db.session.commit()

    flash(
        "Task added successfully.",
        "success"
    )

    return redirect(
        url_for("tasks.task_list")
    )


# =========================================================
# EDIT TASK PAGE
# =========================================================

@tasks_bp.route("/edit/<int:task_id>", methods=["GET"])
def edit_task(task_id):

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    task = Task.query.filter_by(
        id=task_id,
        user_id=session["user_id"]
    ).first_or_404()

    return render_template(
        "edit_task.html",
        task=task
    )


# =========================================================
# UPDATE TASK
# =========================================================

@tasks_bp.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    task = Task.query.filter_by(
        id=task_id,
        user_id=session["user_id"]
    ).first_or_404()

    title = request.form.get(
        "title",
        ""
    ).strip()

    if not title:

        flash(
            "Task title cannot be empty.",
            "error"
        )

        return redirect(
            url_for(
                "tasks.edit_task",
                task_id=task.id
            )
        )

    task.title = title

    db.session.commit()

    flash(
        "Task updated successfully.",
        "success"
    )

    return redirect(
        url_for("tasks.task_list")
    )


# =========================================================
# UPDATE TASK STATUS
# =========================================================

@tasks_bp.route(
    "/status/<int:task_id>",
    methods=["POST"]
)
def update_status(task_id):

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    task = Task.query.filter_by(
        id=task_id,
        user_id=session["user_id"]
    ).first_or_404()

    action = request.form.get("action")

    if action == "start":

        task.status = "in_progress"

    elif action == "complete":

        task.status = "completed"

    elif action == "undo":

        task.status = "pending"

    db.session.commit()

    return redirect(
        url_for("tasks.task_list")
    )


# =========================================================
# CLEAR ALL TASKS
# =========================================================

@tasks_bp.route(
    "/clear",
    methods=["POST"]
)
def clear_tasks():

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    Task.query.filter_by(
        user_id=session["user_id"]
    ).delete()

    db.session.commit()

    flash(
        "All tasks have been deleted.",
        "success"
    )

    return redirect(
        url_for("tasks.task_list")
    )

@tasks_bp.route(
    "/delete/<int:task_id>",
    methods=["POST"]
)
def delete_task(task_id):

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    task = Task.query.filter_by(
        id=task_id,
        user_id=session["user_id"]
    ).first_or_404()

    db.session.delete(task)
    db.session.commit()

    flash(
        "Task deleted successfully.",
        "success"
    )

    return redirect(
        url_for("tasks.task_list")
    )