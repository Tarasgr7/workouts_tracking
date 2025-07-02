from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ExerciseBase(BaseModel):
    type_id: int
    name: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    duration_min: Optional[float] = None


class ExerciseCreate(ExerciseBase):
    workout_id: int


class ExerciseRead(ExerciseBase):
    id: int
    workout_id: int
    created_at: datetime

    class Config:
        orm_mode = True
