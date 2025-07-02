from sqlalchemy.orm import Session
from db.models.workout_model import Workout
from service.schemas.workout_shemas import WorkoutCreate


def get_workout_by_id(db: Session, workout_id: int, user_id: int):
    return (
        db.query(Workout)
        .filter(Workout.id == workout_id, Workout.user_id == user_id)
        .first()
    )


def get_all_workouts(db: Session, user_id: int):
    return db.query(Workout).filter(Workout.user_id == user_id).all()


def create_workout(db: Session, workout: WorkoutCreate, user_id: int):
    db_workout = Workout(**workout.dict(), user_id=user_id)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


def update_workout(db: Session, db_workout: Workout, update_data: dict, user_id: int):
    for key, value in update_data.items():
        setattr(db_workout, key, value)
    db.commit()
    db.refresh(db_workout)
    return db_workout


def delete_workout(db: Session, db_workout: Workout, user_id: int):
    db.delete(db_workout)
    db.commit()
