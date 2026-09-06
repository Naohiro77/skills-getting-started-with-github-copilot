def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_details(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert "Basketball Club" in activities
    assert activities["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_student_to_activity(client):
    email = "student@mergington.edu"

    response = client.post(
        "/activities/Basketball Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for Basketball Club"
    }
    assert client.get("/activities").json()["Basketball Club"]["participants"] == [
        email
    ]


def test_duplicate_signup_is_rejected(client):
    email = "student@mergington.edu"
    endpoint = "/activities/Basketball Club/signup"

    first_response = client.post(endpoint, params={"email": email})
    duplicate_response = client.post(endpoint, params={"email": email})

    assert first_response.status_code == 200
    assert duplicate_response.status_code == 400
    assert duplicate_response.json() == {
        "detail": "Student already signed up for this activity"
    }
    assert client.get("/activities").json()["Basketball Club"]["participants"] == [
        email
    ]


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
