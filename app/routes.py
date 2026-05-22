"""API routes for the Smart Task Manager application."""

from flask import Blueprint, jsonify, request


main = Blueprint("main", __name__)

tasks = []
next_id = 1


@main.route("/", methods=["GET"])
def home():
    """Return a welcome message for the API."""
    return jsonify({
        "message": "Smart Task Manager API is running",
        "version": "1.0.0"
    }), 200


@main.route("/health", methods=["GET"])
def health():
    """Return application health status."""
    return jsonify({
        "status": "ok",
        "service": "smart-task-manager-api"
    }), 200


@main.route("/tasks", methods=["GET"])
def get_tasks():
    """Return all available tasks."""
    return jsonify(tasks), 200


@main.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task."""
    global next_id

    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({
            "error": "Task title is required"
        }), 400

    task = {
        "id": next_id,
        "title": data["title"],
        "status": data.get("status", "pending")
    }

    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


@main.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update an existing task by ID."""
    data = request.get_json()

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data.get("title", task["title"])
            task["status"] = data.get("status", task["status"])
            return jsonify(task), 200

    return jsonify({
        "error": "Task not found"
    }), 404


@main.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete an existing task by ID."""
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return jsonify({
                "message": "Task deleted successfully"
            }), 200

    return jsonify({
        "error": "Task not found"
    }), 404
