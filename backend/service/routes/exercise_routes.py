from fastapi import APIRouter, HTTPException, status, Depends
from db.dependencies import db_dependency
from service.utils.auth_utils import user_dependency
from service.utils.exercise_utils import (
    get_exercise_by_id,
    get_exercises_for_workout,
    create_exercise,
    update_exercise,
    delete_exercise,
)
from service.schemas.exercise_schemas import ExerciseCreate, ExerciseRead

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get(
    "/workouts/{workout_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[ExerciseRead],
)
def get_all(
    workout_id: int,
    db=Depends(db_dependency),
    user=Depends(user_dependency),
):
    return get_exercises_for_workout(db, workout_id, user.get("id"))


@router.get(
    "/{exercise_id}", status_code=status.HTTP_200_OK, response_model=ExerciseRead
)
def get_by_id(
    exercise_id: int,
    db=Depends(db_dependency),
    user=Depends(user_dependency),
):
    ex = get_exercise_by_id(db, exercise_id, user.get("id"))
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return ex


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ExerciseRead)
def create(
    ex_data: ExerciseCreate,
    db=Depends(db_dependency),
    user=Depends(user_dependency),
):
    ex, error = create_exercise(db, ex_data, user.get("id"))
    if error:
        raise HTTPException(status_code=400, detail=error)
    return ex


@router.put(
    "/{exercise_id}", status_code=status.HTTP_200_OK, response_model=ExerciseRead
)
def update(
    exercise_id: int,
    ex_data: ExerciseCreate,
    db=Depends(db_dependency),
    user=Depends(user_dependency),
):
    ex = get_exercise_by_id(db, exercise_id, user.get("id"))
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return update_exercise(db, ex, ex_data.dict())


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    exercise_id: int,
    db=Depends(db_dependency),
    user=Depends(user_dependency),
):
    ex = get_exercise_by_id(db, exercise_id, user.get("id"))
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")
    delete_exercise(db, ex)
    return None
