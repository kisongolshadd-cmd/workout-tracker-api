from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from models import CATEGORIES


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    category = fields.Str(required=True, validate=validate.OneOf(CATEGORIES))
    equipment_needed = fields.Bool(load_default=False)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=1, max=1000), allow_none=True)
    sets = fields.Int(validate=validate.Range(min=1, max=100), allow_none=True)
    duration_seconds = fields.Int(validate=validate.Range(min=1, max=36000), allow_none=True)
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates_schema
    def check_reps_sets_or_duration(self, data, **kwargs):
        has_reps_and_sets = data.get("reps") and data.get("sets")
        has_duration = data.get("duration_seconds")
        if not has_reps_and_sets and not has_duration:
            raise ValidationError(
                "Provide both reps and sets, or a duration_seconds.", "reps"
            )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=600))
    notes = fields.Str(validate=validate.Length(max=500), allow_none=True)
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()