from pydantic import BaseModel
from datetime import date, datetime


class WorkoutBase(BaseModel):
    date: date
    notes: str | None = None


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutRead(WorkoutBase):
    id: int
    created_at: datetime
