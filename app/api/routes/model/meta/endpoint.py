from fastapi import APIRouter
from app.api.routes.model.meta import llama_32_11b_vision_instruct

router = APIRouter(prefix="/meta:")
router.include_router(llama_32_11b_vision_instruct.router)