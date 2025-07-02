from fastapi import APIRouter, HTTPException, Depends
from db.dependencies import db_dependency
from db.models.user_model import User
from db.models.workout_model import Workout
from service.schemas.user_schemas import PublicDashboardSettings
from ..utils.auth_utils import user_dependency, get_user_by_id

router = APIRouter()


@router.patch("/users/me/dashboard-settings", response_model=dict)
def update_dashboard_settings(
    settings: PublicDashboardSettings,
    db=Depends(db_dependency),
    user=Depends(user_dependency),
):
    db_user = get_user_by_id(db, user["id"])
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if settings.public_slug:
        slug_owner = (
            db.query(User).filter(User.public_slug == settings.public_slug).first()
        )
        if slug_owner and slug_owner.id != db_user.id:
            raise HTTPException(status_code=400, detail="Slug already taken")

    db_user.is_public = settings.is_public
    db_user.public_slug = settings.public_slug
    db.commit()
    db.refresh(db_user)

    return {
        "detail": "Dashboard settings updated",
        "public_slug": db_user.public_slug,
        "is_public": db_user.is_public,
    }


@router.get("/dashboard/{slug}", response_model=dict)
def get_public_dashboard(slug: str, db=Depends(db_dependency)):
    user = db.query(User).filter_by(public_slug=slug, is_public=True).first()
    if not user:
        raise HTTPException(status_code=404, detail="Dashboard not found")

    workouts = db.query(Workout).filter_by(user_id=user.id).all()

    return {
        "username": user.username,
        "workouts": [
            {
                "date": w.date,
                "notes": w.notes,
                "exercises": [
                    {
                        "name": e.name,
                        "sets": e.sets,
                        "reps": e.reps,
                        "weight": e.weight,
                        "duration_min": e.duration_min,
                    }
                    for e in w.exercises
                ],
            }
            for w in workouts
        ],
    }
