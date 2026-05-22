from app import create_app
from app.routes import tasks


def setup_function():
    tasks.clear()


def test_create_task():
    app = create_app()
    client = app.test_client()

    response = client.post("/tasks", json={
        "title": "Complete Jenkins pipeline"
    })

    data = response.get_json()

    assert response.status_code == 201
    assert data["title"] == "Complete Jenkins pipeline"
    assert data["status"] == "pending"


def test_get_tasks():
    app = create_app()
    client = app.test_client()

    client.post("/tasks", json={
        "title": "Record demo video"
    })

    response = client.get("/tasks")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Record demo video"


def test_update_task():
    app = create_app()
    client = app.test_client()

    create_response = client.post("/tasks", json={
        "title": "Write report"
    })

    task_id = create_response.get_json()["id"]

    update_response = client.put(f"/tasks/{task_id}", json={
        "status": "completed"
    })

    data = update_response.get_json()

    assert update_response.status_code == 200
    assert data["status"] == "completed"


def test_delete_task():
    app = create_app()
    client = app.test_client()

    create_response = client.post("/tasks", json={
        "title": "Delete this task"
    })

    task_id = create_response.get_json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    data = delete_response.get_json()

    assert delete_response.status_code == 200
    assert data["message"] == "Task deleted successfully"


def test_create_task_without_title():
    app = create_app()
    client = app.test_client()

    response = client.post("/tasks", json={})

    assert response.status_code == 400
    assert response.get_json()["error"] == "Task title is required"
