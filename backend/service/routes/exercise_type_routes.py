from fastapi import APIRouter, HTTPException, status, Depends
from db.dependencies import db_dependency
from service.schemas.exercise_type_schemas import ExerciseTypeCreate, ExerciseTypeRead
from service.utils.exercise_type_utils import (
    get_all_types,
    get_type_by_id,
    create_type,
    update_type,
    delete_type,
)
from db.models.exercise_type_model import ExerciseType
from service.utils.auth_utils import user_dependency

router = APIRouter(
    prefix="/exercise-types",
    tags=["exercise-types"],
    dependencies=[Depends(user_dependency)],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ExerciseTypeRead])
def read_types(db=Depends(db_dependency)):
    return get_all_types(db)


@router.get(
    "/{type_id}", status_code=status.HTTP_200_OK, response_model=ExerciseTypeRead
)
def read_type(type_id: int, db=Depends(db_dependency)):
    ex_type = get_type_by_id(db, type_id)
    if not ex_type:
        raise HTTPException(status_code=404, detail="Exercise type not found")
    return ex_type


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ExerciseTypeRead)
def create_new_type(type_data: ExerciseTypeCreate, db=Depends(db_dependency)):
    existing = (
        db.query(ExerciseType).filter(ExerciseType.name == type_data.name).first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exercise type already exists",
        )
    return create_type(db, type_data)


@router.put(
    "/{type_id}", status_code=status.HTTP_200_OK, response_model=ExerciseTypeRead
)
def update_existing_type(
    type_id: int, type_data: ExerciseTypeCreate, db=Depends(db_dependency)
):
    db_type = get_type_by_id(db, type_id)
    if not db_type:
        raise HTTPException(status_code=404, detail="Exercise type not found")
    return update_type(db, db_type, type_data.name)


@router.delete("/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_type(type_id: int, db=Depends(db_dependency)):
    db_type = get_type_by_id(db, type_id)
    if not db_type:
        raise HTTPException(status_code=404, detail="Exercise type not found")
    delete_type(db, db_type)
    return None
