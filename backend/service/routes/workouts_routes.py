from fastapi import APIRouter, HTTPException, status, Depends
from db.dependencies import db_dependency
from service.schemas.workout_shemas import WorkoutCreate, WorkoutRead
from service.utils.auth_utils import user_dependency
from service.utils.workouts_utils import (
    get_all_workouts,
    get_workout_by_id,
    create_workout,
    update_workout,
    delete_workout,
)

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"],
    dependencies=[Depends(user_dependency)],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[WorkoutRead])
def read_workouts(db=Depends(db_dependency), user=Depends(user_dependency)):
    return get_all_workouts(db, user.get("id"))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=WorkoutRead)
def create_new_workout(
    workout: WorkoutCreate, db=Depends(db_dependency), user=Depends(user_dependency)
):
    return create_workout(db, workout, user.get("id"))


@router.get("/{workout_id}", status_code=status.HTTP_200_OK, response_model=WorkoutRead)
def read_workout(
    workout_id: int, db=Depends(db_dependency), user=Depends(user_dependency)
):
    workout = get_workout_by_id(db, workout_id, user.get("id"))
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@router.put("/{workout_id}", status_code=status.HTTP_200_OK, response_model=WorkoutRead)
def update_existing_workout(
    workout_id: int,
    workout: WorkoutCreate,
    db=Depends(db_dependency),
    user=Depends(user_dependency),
):
    db_workout = get_workout_by_id(db, workout_id, user.get("id"))
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return update_workout(db, db_workout, workout.dict(), user.get("id"))


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_workout(
    workout_id: int, db=Depends(db_dependency), user=Depends(user_dependency)
):
    db_workout = get_workout_by_id(db, workout_id, user.get("id"))
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    delete_workout(db, db_workout, user.get("id"))
    return None
