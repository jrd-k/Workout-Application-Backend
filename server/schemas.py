from marshmallow import Schema, fields, validate, ValidationError, validates_schema

from models import ALLOWED_CATEGORIES

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(load_only=True)
    exercise_id = fields.Int()
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))

    exercise = fields.Nested(
        "ExerciseSchema", only=("id", "name", "category", "equipment_needed"), dump_only=True
    )

    @validates_schema
    def validate_has_metric(self, data, **kwargs):
        if not any(
            data.get(field) is not None
            for field in ("reps", "sets", "duration_seconds")
        ):
            raise ValidationError(
                "At least one of reps, sets, or duration_seconds is required."
            )

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    category = fields.Str(
        required=True, validate=validate.OneOf(sorted(ALLOWED_CATEGORIES))
    )
    equipment_needed = fields.Bool(load_default=False)

    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema, exclude=("exercise",)), dump_only=True
    )

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True)

    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema, exclude=("workout_id",)), dump_only=True
    )

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
