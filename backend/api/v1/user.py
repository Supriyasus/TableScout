from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/preferences")
def get_user_preferences():
    return {"message": "User API working"}
