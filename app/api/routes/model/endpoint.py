from fastapi import APIRouter
from app.api.routes.model import auto

router = APIRouter()
router.include_router(auto.router)