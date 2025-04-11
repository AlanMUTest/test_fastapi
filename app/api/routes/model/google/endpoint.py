from fastapi import APIRouter
from app.api.routes.model.google import gemini_20_flash_exp
from app.api.routes.model.google import gemini_25_pro_exp

router = APIRouter(prefix="/google:")
router.include_router(gemini_20_flash_exp.router)
router.include_router(gemini_25_pro_exp.router)