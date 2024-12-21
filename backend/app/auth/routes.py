from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.models import User
from app.auth.schemas import UserCreate, UserLogin  # Import schemas
from app.auth.utils import create_token, verify_password  # Import utilities
from app.auth.dependencies import get_current_user  # Import get_current_user dependency

router = APIRouter()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    hashed_password = verify_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_token({"sub": new_user.id})
    return {"message": "User registered successfully", "token": token}

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token({"sub": db_user.id})
    return {"message": "Login successful", "token": token}

@router.post("/follow/{user_id}")
async def follow_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user_to_follow = db.query(User).filter(User.id == user_id).first()
    if not user_to_follow:
        raise HTTPException(status_code=404, detail="User not found")
    if user_to_follow.id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    if user_to_follow in current_user.following:
        raise HTTPException(status_code=400, detail="Already following this user")

    current_user.following.append(user_to_follow)
    db.commit()
    return {"message": f"Started following {user_to_follow.username}"}

@router.post("/unfollow/{user_id}")
async def unfollow_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user_to_unfollow = db.query(User).filter(User.id == user_id).first()
    if not user_to_unfollow:
        raise HTTPException(status_code=404, detail="User not found")
    if user_to_unfollow.id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot unfollow yourself")

    if user_to_unfollow not in current_user.following:
        raise HTTPException(status_code=400, detail="Not following this user")

    current_user.following.remove(user_to_unfollow)
    db.commit()
    return {"message": f"Stopped following {user_to_unfollow.username}"}
