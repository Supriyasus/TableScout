from fastapi import APIRouter
from .v1 import places, booking, user

router = APIRouter(prefix="/api/v1")

router.include_router(places.router)
router.include_router(booking.router)
router.include_router(user.router)
