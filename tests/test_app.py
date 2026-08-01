from datetime import date

import pytest

from server.app import app, db
from server.models import Exercise, Workout, WorkoutExercise


@pytest.fixture(autouse=True)
def client_and_db():
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_get_workouts_returns_empty_list(client_and_db):
    response = client_and_db.get("/workouts")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_workout_returns_created_workout(client_and_db):
    response = client_and_db.post(
        "/workouts",
        json={"date": "2026-08-01", "duration_minutes": 30, "notes": "Leg day"},
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["duration_minutes"] == 30
    assert payload["notes"] == "Leg day"
    assert Workout.query.count() == 1


def test_create_exercise_returns_created_exercise(client_and_db):
    response = client_and_db.post(
        "/exercises",
        json={"name": "Squat", "category": "strength", "equipment_needed": True},
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["name"] == "Squat"
    assert payload["category"] == "strength"
    assert Exercise.query.count() == 1


def test_add_exercise_to_workout_requires_a_metric(client_and_db):
    workout = Workout(date=date(2026, 8, 1), duration_minutes=20)
    exercise = Exercise(name="Push Up", category="strength")
    db.session.add_all([workout, exercise])
    db.session.commit()

    response = client_and_db.post(
        f"/workouts/{workout.id}/exercises/{exercise.id}/workout_exercises",
        json={},
    )

    assert response.status_code == 400
    assert "At least one of reps, sets, or duration_seconds is required." in response.get_json()["errors"]["_schema"]


def test_add_exercise_to_workout_creates_join_record(client_and_db):
    workout = Workout(date=date(2026, 8, 1), duration_minutes=20)
    exercise = Exercise(name="Push Up", category="strength")
    db.session.add_all([workout, exercise])
    db.session.commit()

    response = client_and_db.post(
        f"/workouts/{workout.id}/exercises/{exercise.id}/workout_exercises",
        json={"reps": 10, "sets": 3},
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["reps"] == 10
    assert payload["sets"] == 3
    assert WorkoutExercise.query.count() == 1
