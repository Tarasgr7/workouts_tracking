from sqlalchemy.orm import Session
from db.models.exercise_model import Exercise
from db.models.workout_model import Workout
from db.models.exercise_type_model import ExerciseType
from service.schemas.exercise_schemas import ExerciseCreate


def get_exercise_by_id(db: Session, ex_id: int, user_id: int):
    return (
        db.query(Exercise)
        .join(Workout)
        .filter(Exercise.id == ex_id, Workout.user_id == user_id)
        .first()
    )


def get_exercises_for_workout(db: Session, workout_id: int, user_id: int):
    return (
        db.query(Exercise)
        .join(Workout)
        .filter(Exercise.workout_id == workout_id, Workout.user_id == user_id)
        .all()
    )


def create_exercise(db: Session, data: ExerciseCreate, user_id: int):
    workout = db.query(Workout).filter_by(id=data.workout_id, user_id=user_id).first()
    if not workout:
        return None, "Workout not found or not yours"

    ex_type = db.query(ExerciseType).filter_by(id=data.type_id).first()
    if not ex_type:
        return None, "Exercise type not found"

    exercise = Exercise(**data.dict())
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise, None


def update_exercise(db: Session, exercise: Exercise, update_data: dict):
    for key, value in update_data.items():
        setattr(exercise, key, value)
    db.commit()
    db.refresh(exercise)
    return exercise


def delete_exercise(db: Session, exercise: Exercise):
    db.delete(exercise)
    db.commit()
