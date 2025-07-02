from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.dependencies import Base


class ExerciseType(Base):
    __tablename__ = "exercise_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    exercises = relationship("Exercise", back_populates="type")
