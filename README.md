# Workout Tracker API

## Description
A backend API for a personal-trainer workout app, built with Flask, SQLAlchemy and Marshmallow.
Trainers can create workouts, create reusable exercises, and add exercises to workouts with
reps and sets or a duration.

Models: `Exercise`, `Workout`, and `WorkoutExercise` (join table, many-to-many).

Validations:
- Table constraints: unique exercise name, name length, allowed categories, positive durations, unique workout and exercise pair
- Model validations (`@validates`): exercise name and category, workout duration and notes, reps, sets and duration
- Schema validations (Marshmallow): length and range checks, allowed values, valid date, and a custom rule that reps and sets, or a duration, must be given

## Installation
```
git clone <your-repo-url>
cd workout_app
pipenv install
pipenv shell
export FLASK_APP=app.py
flask db upgrade
python seed.py
```

## Run
```
python app.py
```
The API runs on http://localhost:5555

## Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| GET | /workouts | List all workouts with their exercises |
| GET | /workouts/<id> | Show one workout with its exercises, reps, sets and duration |
| POST | /workouts | Create a workout: {"date": "2026-10-25", "duration_minutes": 40, "notes": "..."} |
| DELETE | /workouts/<id> | Delete a workout |
| GET | /exercises | List all exercises |
| GET | /exercises/<id> | Show one exercise |
| POST | /exercises | Create an exercise: {"name": "Lunge", "category": "strength", "equipment_needed": false} |
| DELETE | /exercises/<id> | Delete an exercise |
| POST | /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises | Add an exercise to a workout: {"reps": 10, "sets": 3} or {"duration_seconds": 60} |

Errors return JSON: 400 for invalid data, 404 when not found, 409 for duplicates.