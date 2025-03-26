from fastapi import APIRouter
from app.api.routes.model.mistral import mistral_small_31_24b_instruct

router = APIRouter(prefix="/mistral:")
router.include_router(mistral_small_31_24b_instruct.router)