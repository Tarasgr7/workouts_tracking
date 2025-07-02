from datetime import datetime, date
from pydantic import BaseModel
from typing import List, Optional


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class PublicDashboardSettings(BaseModel):
    is_public: bool
    public_slug: Optional[str]


class WorkoutPublic(BaseModel):
    id: int
    date: date
    notes: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class UserPublicDashboard(BaseModel):
    username: str
    public_slug: str
    workouts: List[WorkoutPublic]

    class Config:
        orm_mode = True
