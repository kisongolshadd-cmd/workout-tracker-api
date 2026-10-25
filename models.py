from sqlalchemy.orm import validates
from config import db

CATEGORIES = ["strength", "cardio", "flexibility", "balance"]


class Exercise(db.Model):
    __tablename__ = "exercises"

    __table_args__ = (
        db.CheckConstraint("length(name) >= 2", name="check_exercise_name_length"),
        db.CheckConstraint(
            "category IN ('strength', 'cardio', 'flexibility', 'balance')",
            name="check_exercise_category",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan"
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters long.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if value not in CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(CATEGORIES)}.")
        return value


class Workout(db.Model):
    __tablename__ = "workouts"

    __table_args__ = (
        db.CheckConstraint("duration_minutes > 0", name="check_workout_duration"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="workout", cascade="all, delete-orphan"
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Workout duration must be greater than 0 minutes.")
        return value

    @validates("notes")
    def validate_notes(self, key, value):
        if value is not None and len(value) > 500:
            raise ValueError("Notes cannot be longer than 500 characters.")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    __table_args__ = (
        db.UniqueConstraint("workout_id", "exercise_id", name="unique_workout_exercise"),
        db.CheckConstraint("reps IS NULL OR reps > 0", name="check_reps_positive"),
        db.CheckConstraint("sets IS NULL OR sets > 0", name="check_sets_positive"),
        db.CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds > 0",
            name="check_duration_positive",
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

    @validates("reps", "sets", "duration_seconds")
    def validate_positive(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f"{key} must be greater than 0.")
        return value