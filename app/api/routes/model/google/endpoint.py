from fastapi import APIRouter
from api.routes.model.google import gemini_20_flash_exp

google_router = APIRouter(prefix="/google:")
google_router.include_router(gemini_20_flash_exp.router)
