#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Seeding exercises...")
    push_ups = Exercise(name="Push Ups", category="strength", equipment_needed=False)
    squats = Exercise(name="Squats", category="strength", equipment_needed=False)
    running = Exercise(name="Running", category="cardio", equipment_needed=False)
    bench_press = Exercise(name="Bench Press", category="strength", equipment_needed=True)
    yoga_stretch = Exercise(name="Yoga Stretch", category="flexibility", equipment_needed=False)

    db.session.add_all([push_ups, squats, running, bench_press, yoga_stretch])
    db.session.commit()

    print("Seeding workouts...")
    workout_1 = Workout(date=date(2026, 7, 20), duration_minutes=45, notes="Morning strength session")
    workout_2 = Workout(date=date(2026, 7, 22), duration_minutes=30, notes="Quick cardio session")
    workout_3 = Workout(date=date(2026, 7, 24), duration_minutes=60, notes="Full body + stretch")

    db.session.add_all([workout_1, workout_2, workout_3])
    db.session.commit()

    print("Seeding workout_exercises (join records)...")
    workout_exercises = [
        WorkoutExercise(workout_id=workout_1.id, exercise_id=push_ups.id, reps=15, sets=3),
        WorkoutExercise(workout_id=workout_1.id, exercise_id=squats.id, reps=12, sets=4),
        WorkoutExercise(workout_id=workout_1.id, exercise_id=bench_press.id, reps=8, sets=3),
        WorkoutExercise(workout_id=workout_2.id, exercise_id=running.id, duration_seconds=1800),
        WorkoutExercise(workout_id=workout_3.id, exercise_id=squats.id, reps=10, sets=3),
        WorkoutExercise(workout_id=workout_3.id, exercise_id=yoga_stretch.id, duration_seconds=600),
    ]

    db.session.add_all(workout_exercises)
    db.session.commit()

    print("Done seeding!")
