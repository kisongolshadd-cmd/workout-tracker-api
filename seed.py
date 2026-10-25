from datetime import date

from config import app, db
from models import Exercise, Workout, WorkoutExercise

with app.app_context():
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    squat = Exercise(name="Squat", category="strength", equipment_needed=True)
    pushup = Exercise(name="Push-up", category="strength", equipment_needed=False)
    running = Exercise(name="Running", category="cardio", equipment_needed=False)
    plank = Exercise(name="Plank", category="strength", equipment_needed=False)
    yoga = Exercise(name="Yoga Flow", category="flexibility", equipment_needed=False)
    db.session.add_all([squat, pushup, running, plank, yoga])

    leg_day = Workout(date=date(2026, 10, 20), duration_minutes=45, notes="Leg day")
    cardio_day = Workout(date=date(2026, 10, 22), duration_minutes=30, notes="Morning cardio")
    core_day = Workout(date=date(2026, 10, 24), duration_minutes=25, notes="Core and stretch")
    db.session.add_all([leg_day, cardio_day, core_day])

    db.session.add_all([
        WorkoutExercise(workout=leg_day, exercise=squat, reps=10, sets=4),
        WorkoutExercise(workout=leg_day, exercise=plank, duration_seconds=60),
        WorkoutExercise(workout=cardio_day, exercise=running, duration_seconds=1200),
        WorkoutExercise(workout=core_day, exercise=pushup, reps=15, sets=3),
        WorkoutExercise(workout=core_day, exercise=plank, duration_seconds=90),
        WorkoutExercise(workout=core_day, exercise=yoga, duration_seconds=600),
    ])

    db.session.commit()
    print("Done seeding!")