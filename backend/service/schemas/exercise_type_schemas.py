from pydantic import BaseModel


class ExerciseTypeBase(BaseModel):
    name: str


class ExerciseTypeCreate(ExerciseTypeBase):
    pass


class ExerciseTypeRead(ExerciseTypeBase):
    id: int

    class Config:
        orm_mode = True
