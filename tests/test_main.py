# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Immersion Tracker"}

def test_create_log(mocker):
    mock_insert = mocker.patch("main.supabase.table")
    mock_insert.return_value.insert.return_value.execute.return_value.data = [{"id": "fake_id"}]
    
    response = client.post("/log", json={
        "type": "reading",
        "duration": 20,
        "description": "Test reading"
    })
    assert response.status_code == 200

def test_integration_create_and_get_log():
    # Post
    post_resp = client.post("/log", json={"type": "reading", "duration": 30, "description": "Integration test"})
    assert post_resp.status_code == 200

    # Get
    get_resp = client.get("/logs")
    assert get_resp.status_code == 200
    assert any(log["description"] == "Integration test" for log in get_resp.json())


def test_full_crud():
    data = {"type": "writing", "duration": 15, "description": "API test"}
    post = client.post("/log", json=data)
    log_id = post.json()[0]["id"]

    get = client.get("/logs")
    assert any(log["id"] == log_id for log in get.json())

    update = client.put(f"/log/{log_id}", json={"type": "writing", "duration": 20, "description": "updated"})
    assert update.status_code == 200

    delete = client.delete(f"/log/{log_id}")
    assert delete.status_code == 200