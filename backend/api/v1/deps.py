# api/deps.py
from backend.db.session import SessionLocal
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.auth.security import get_user_id_from_token

security = HTTPBearer()


def get_db():
    """
    FastAPI dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    FastAPI dependency to extract and validate user from JWT token
    Returns user_id
    """
    token = credentials.credentials
    try:
        user_id = get_user_id_from_token(token)
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
