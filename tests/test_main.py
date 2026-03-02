import pytest

# AAA: Arrange-Act-Assert pattern for FastAPI endpoints

def test_get_activities(client):
    # Arrange: client fixture provided
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Confirm participant added
    get_response = client.get("/activities")
    assert email in get_response.json()[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "daniel@mergington.edu"  # Already signed up
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_from_activity(client):
    # Arrange
    activity = "Chess Club"
    email = "daniel@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"
    # Confirm participant removed
    get_response = client.get("/activities")
    assert email not in get_response.json()[activity]["participants"]


def test_unregister_not_registered(client):
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
