from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.models import User
from app.schemas import UserLogin, UserRegister, TokenResponse, UserResponse
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
)
from app.middleware.auth import get_current_active_user
from app.config import settings
from app.utils.errors import (
    UnauthorizedError,
    ForbiddenError,
    ConflictError,
    InternalServerError,
    log_error,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new staff user."""
    try:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ConflictError("User", "Email already registered")

        hashed_pwd = hash_password(user_data.password)
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_pwd,
            full_name=user_data.full_name,
            is_active=True,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except ConflictError:
        raise
    except Exception as e:
        db.rollback()
        log_error("register", e)
        raise InternalServerError(f"Failed to register user: {str(e)}")


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login staff user and return JWT access token."""
    try:
        user = db.query(User).filter(User.email == credentials.email).first()

        if not user or not verify_password(credentials.password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")

        if not user.is_active:
            raise ForbiddenError("User account is inactive")

        access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
        expires_in = settings.access_token_expire_minutes * 60

        response = JSONResponse(
            content={
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": expires_in,
            }
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=not settings.debug,
            samesite="lax",
            max_age=expires_in,
        )
        return response
    except (UnauthorizedError, ForbiddenError):
        raise
    except Exception as e:
        log_error("login", e)
        raise InternalServerError(f"Failed to login: {str(e)}")


@router.post("/logout")
def logout():
    """Logout user by clearing the access token cookie."""
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie(key="access_token", secure=not settings.debug, samesite="lax")
    return response


@router.get("/me", response_model=UserResponse)
def get_current_user(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user info."""
    return current_user
