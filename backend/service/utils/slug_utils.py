import re
import uuid
from sqlalchemy.orm import Session
from db.models import User


def generate_slug_from_username(username: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", username.lower()).strip("-")
    return slug or str(uuid.uuid4())


def ensure_unique_slug(db: Session, base_slug: str) -> str:
    slug = base_slug
    suffix = 1
    while db.query(User).filter(User.public_slug == slug).first():
        slug = f"{base_slug}-{suffix}"
        suffix += 1
    return slug
