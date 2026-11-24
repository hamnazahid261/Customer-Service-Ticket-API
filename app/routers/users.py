
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app import models, schemas
from app.database import get_db
from app.security import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])

# Initialize secure password hashing
password_hash = PasswordHash.recommended()


# 1. Register a new customer
@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password before saving
    hashed_password = password_hash.hash(user.password)

    # Public registration always creates a customer
    new_user = models.User(
        name=user.name,
        email=user.email,
        role="customer",
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# 2. Get all users (support agent only)
@router.get("/", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "support_agent":
        raise HTTPException(
            status_code=403,
            detail="Only support agents can view all users"
        )

    users = db.query(models.User).all()

    return users


# 3. Get user by ID
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Customers can only view their own profile
    if (
        current_user.role == "customer"
        and current_user.id != user_id
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to view this user"
        )

    if current_user.role not in ["customer", "support_agent"]:
        raise HTTPException(
            status_code=403,
            detail="Invalid user role"
        )

    return user
