from datetime import date, timedelta
from typing import Any, cast

from flask import Blueprint, Response, jsonify, request

from .models import Task, User, db
from .utils import calculate_next_due_date, calculate_snooze_days

api = Blueprint("api", __name__)


@api.route("/users", methods=["GET"])
def get_users() -> Response:
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@api.route("/login", methods=["POST"])
def login() -> tuple[Response, int] | Response:
    data = cast(dict[str, Any], request.json)
    if not data or "username" not in data:
        return jsonify({"error": "Missing username"}), 400

    username = data["username"].strip()
    user = User.query.filter(User.username.ilike(username)).first()
    if not user:
        user = User(username=username.capitalize())
        db.session.add(user)
        db.session.commit()

    return jsonify(user.to_dict())


@api.route("/tasks", methods=["GET"])
def get_tasks() -> Response:
    user_id = request.args.get("user_id")
    if user_id:
        today = date.today()
        future_limit = today + timedelta(days=3)
        tasks = (
            Task.query.filter(
                Task.users.any(User.id == int(user_id)),
                Task.status == "pending",
                Task.due_date <= future_limit,
            )
            .order_by(Task.due_date)
            .all()
        )
    else:
        tasks = Task.query.order_by(Task.due_date).all()

    return jsonify([t.to_dict() for t in tasks])


@api.route("/tasks", methods=["POST"])
def create_task() -> tuple[Response, int]:
    data = cast(dict[str, Any], request.json)

    task = Task(
        title=data["title"],
        due_date=date.fromisoformat(data["due_date"]),
        details=data.get("details"),
        emoji=data.get("emoji", "📝"),
        is_recurring=data.get("is_recurring", False),
        interval_type=data.get("interval_type"),
        interval_value=data.get("interval_value"),
        specific_day=data.get("specific_day"),
    )

    if "user_ids" in data:
        users = User.query.filter(User.id.in_(data["user_ids"])).all()
        task.users = users

    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@api.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id: int) -> Response:
    task = Task.query.get_or_404(task_id)
    data = cast(dict[str, Any], request.json)

    if "title" in data:
        task.title = data["title"]
    if "user_ids" in data:
        users = User.query.filter(User.id.in_(data["user_ids"])).all()
        task.users = users
    if "due_date" in data:
        task.due_date = date.fromisoformat(data["due_date"])
    if "details" in data:
        task.details = data["details"]
    if "emoji" in data:
        task.emoji = data["emoji"]
    if "is_recurring" in data:
        task.is_recurring = data["is_recurring"]
    if "interval_type" in data:
        task.interval_type = data["interval_type"]
    if "interval_value" in data:
        task.interval_value = data["interval_value"]
    if "specific_day" in data:
        task.specific_day = data["specific_day"]

    db.session.commit()
    return jsonify(task.to_dict())


@api.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int) -> tuple[str, int]:
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return "", 204


@api.route("/tasks/<int:task_id>/action", methods=["POST"])
def task_action(task_id: int) -> Response:
    task = Task.query.get_or_404(task_id)
    data = cast(dict[str, Any], request.json)
    action = data.get("action")
    today = date.today()

    if "details" in data:
        task.details = data["details"]

    if action == "done":
        if not task.is_recurring:
            task.status = "done"
        else:
            task.due_date = calculate_next_due_date(
                from_date=today,
                interval_type=task.interval_type,
                interval_value=task.interval_value,
                specific_day=task.specific_day,
            )
            task.status = "pending"

    elif action == "snooze":
        snooze_days = 1
        if task.is_recurring and task.interval_type and task.interval_value:
            snooze_days = calculate_snooze_days(task.interval_type, task.interval_value)
        task.due_date = today + timedelta(days=snooze_days)

    elif action == "early_done":  # From Admin view
        if task.is_recurring:
            task.due_date = calculate_next_due_date(
                from_date=today,
                interval_type=task.interval_type,
                interval_value=task.interval_value,
                specific_day=task.specific_day,
                force_at_least_7_days=True,
            )
            task.status = "pending"
        else:
            task.status = "done"

    db.session.commit()
    return jsonify(task.to_dict())
