from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.dependencies import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("exercise_types.id"), nullable=False)

    name = Column(String(100), nullable=False)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)
    duration_min = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    workout = relationship("Workout", back_populates="exercises")
    type = relationship("ExerciseType", back_populates="exercises")
