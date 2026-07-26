from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

db = SQLAlchemy()

ALLOWED_CATEGORIES = {"cardio", "strength", "flexibility", "balance", "other"}


class Exercise(db.Model):
    __tablename__ = "exercises"

    __table_args__ = (
        UniqueConstraint("name", name="uq_exercise_name"),
        CheckConstraint(
            "category IN ('cardio','strength','flexibility','balance','other')",
            name="ck_exercise_category",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        viewonly=True,
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be blank.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if value not in ALLOWED_CATEGORIES:
            raise ValueError(f"category must be one of {sorted(ALLOWED_CATEGORIES)}")
        return value

    def __repr__(self):
        return f"<Exercise {self.id} {self.name}>"


class Workout(db.Model):
    __tablename__ = "workouts"

    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="ck_workout_duration_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, server_default=func.now())
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        viewonly=True,
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError("duration_minutes must be a positive integer.")
        return value

    def __repr__(self):
        return f"<Workout {self.id} {self.date}>"


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    __table_args__ = (
        CheckConstraint(
            "(reps IS NOT NULL) OR (sets IS NOT NULL) OR (duration_seconds IS NOT NULL)",
            name="ck_workout_exercise_has_metric",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("reps must be a positive integer.")
        return value

    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("sets must be a positive integer.")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("duration_seconds must be a positive integer.")
        return value

    def __repr__(self):
        return f"<WorkoutExercise workout={self.workout_id} exercise={self.exercise_id}>"