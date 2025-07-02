# main.py
from fastapi import FastAPI
from db.dependencies import Base, engine
from service.routes.auth_routes import router as auth_router
from service.routes.workouts_routes import router as workout_router
from service.routes.exercise_type_routes import router as exercise_type_router
from service.routes.exercise_routes import router as exercise_router
from service.routes.dashboards_routes import router as dashboards_routes

app = FastAPI()


@app.on_event("startup")
def on_startup():
    print("⏳ Creating tables if not exist...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables ready.")


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(workout_router, prefix="/workout", tags=["Workout"])
app.include_router(
    exercise_type_router, prefix="/exercise-type", tags=["Exercise-type"]
)
app.include_router(exercise_router, prefix="/exercise", tags=["Exercise"])
app.include_router(dashboards_routes, prefix="/dashboard", tags=["Public Dashboard"])
