from fastapi import APIRouter, status, HTTPException, Depends
from db.models.user_model import User
from db.dependencies import logger, db_dependency
from service.schemas.user_schemas import UserCreate, Token
from ..utils.auth_utils import (
    validate_password,
    hash_password,
    authenticate_user,
    create_access_token,
)
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from service.utils.slug_utils import generate_slug_from_username, ensure_unique_slug
from typing import Annotated

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: db_dependency):
    logger.info(f"Реєстрація нового користувача: {user.username}")

    if db.query(User).filter_by(username=user.username).first():
        logger.warning("This username is already taken.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already taken.",
        )
    if db.query(User).filter_by(email=user.email).first():
        logger.warning("Email вже зареєстрований")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    validate_password(user.password)

    base_slug = generate_slug_from_username(user.username)
    unique_slug = ensure_unique_slug(db, base_slug)

    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.password),
        public_slug=unique_slug,
        is_public=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(
        f"Користувача {user.email} зареєстровано успішно з slug='{unique_slug}'"
    )
    return {
        "message": "Користувач був успішно зареєстрований",
        "public_slug": unique_slug,
    }


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    logger.info(f"Аутентифікація користувача: {form_data.username}")

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        logger.warning("Не вдалося автентифікувати користувача")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )

    token = create_access_token(user.email, user.id, timedelta(minutes=20))

    logger.info(f"Користувач {user.email} успішно отримав токен")
    return {"access_token": token, "token_type": "bearer"}
