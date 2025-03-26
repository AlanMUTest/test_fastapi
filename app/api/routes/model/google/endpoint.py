from fastapi import APIRouter
from app.api.routes.model.google import gemini_20_flash_exp
from app.api.routes.model.google import gemini_20_pro_exp_02_05

router = APIRouter(prefix="/google:")
router.include_router(gemini_20_flash_exp.router)
router.include_router(gemini_20_pro_exp_02_05.router)