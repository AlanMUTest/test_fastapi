from fastapi import APIRouter
from app.api.routes.model.alibaba import qwen25_vl_72b_instruct

router = APIRouter(prefix="/qwen:")
router.include_router(qwen25_vl_72b_instruct.router)