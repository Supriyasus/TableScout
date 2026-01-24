from backend.auth.security import create_access_token, hash_password, verify_password
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.api.v1.deps import get_db
from backend.db.models import User, UserPreference
from backend.db.crud import create_or_update_user_preference
import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    username: str
    password: str


class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str


@router.post("/signup", response_model=TokenResponse)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    # Check if user already exists
    existing = db.query(User).filter(User.id == request.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # Hash the password
    hashed_pw = hash_password(request.password)

    # Create user record
    new_user = User(
        id=request.username,   # or str(uuid.uuid4()) if you want random IDs
        email=request.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Initialize empty preferences for this user
    create_or_update_user_preference(db, user_id=new_user.id, preferences={"place_type_affinity": {}})

    # Create JWT token
    access_token = create_access_token(data={"sub": new_user.id})
    return TokenResponse(access_token=access_token, user_id=new_user.id)


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Check if user exists (by username OR email)
    user = db.query(User).filter(
        (User.id == request.username) | (User.email == request.username)
    ).first()

    if not user:
        print(f"DEBUG: User '{request.username}' not found in database (checked by username and email)")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Verify password
    password_correct = verify_password(request.password, user.hashed_password)
    print(f"DEBUG: User '{request.username}' found (id={user.id}). Password correct: {password_correct}")
    
    if not password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Create JWT token
    access_token = create_access_token(data={"sub": user.id})

    return TokenResponse(
        access_token=access_token,
        user_id=user.id
    )
