from sqlalchemy.orm import Session
from db.models.user_model import User
from fastapi import HTTPException, status


def get_public_dashboard(db: Session, slug: str):
    user = db.query(User).filter(User.public_slug == slug).first()
    if not user or not user.is_public:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Public dashboard not available",
        )
    return user
