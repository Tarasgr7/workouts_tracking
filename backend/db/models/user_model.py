from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from db.dependencies import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_public = Column(Boolean, default=False)
    public_slug = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    workouts = relationship(
        "Workout", back_populates="user", cascade="all, delete-orphan"
    )


User.workouts = relationship("Workout", back_populates="user")
