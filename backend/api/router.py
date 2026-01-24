from fastapi import APIRouter
from backend.api.v1 import places, booking, user, auth

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(places.router)
router.include_router(booking.router)
router.include_router(user.router)
