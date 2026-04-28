from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities_returns_activity_data():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_adds_participant_to_activity():
    email = "test.signup@mergington.edu"
    activity_name = "Chess Club"
    participants = activities[activity_name]["participants"]
    if email in participants:
        participants.remove(email)

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email in participants


def test_signup_rejects_duplicate_participant():
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_removes_participant_from_activity():
    activity_name = "Programming Class"
    email = "test.unregister@mergington.edu"
    participants = activities[activity_name]["participants"]
    if email not in participants:
        participants.append(email)

    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in participants


def test_unregister_rejects_missing_participant():
    response = client.delete(
        "/activities/Programming Class/unregister",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered"
