from sqlalchemy.orm import Session
from db.models.exercise_type_model import ExerciseType
from service.schemas.exercise_type_schemas import ExerciseTypeCreate


def get_all_types(db: Session):
    return db.query(ExerciseType).all()


def get_type_by_id(db: Session, type_id: int):
    return db.query(ExerciseType).filter(ExerciseType.id == type_id).first()


def create_type(db: Session, type_data: ExerciseTypeCreate):
    db_type = ExerciseType(name=type_data.name)
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type


def update_type(db: Session, db_type: ExerciseType, new_name: str):
    db_type.name = new_name
    db.commit()
    db.refresh(db_type)
    return db_type


def delete_type(db: Session, db_type: ExerciseType):
    db.delete(db_type)
    db.commit()
