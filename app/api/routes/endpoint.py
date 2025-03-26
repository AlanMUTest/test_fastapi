from fastapi import APIRouter
from app.api.routes.model import endpoint as auto_endpoint
from app.api.routes.model.google import endpoint as google_endpoint
from app.api.routes.model.alibaba import endpoint as alibaba_endpoint
from app.api.routes.model.mistral import endpoint as mistral_endpoint
from app.api.routes.model.meta import endpoint as meta_endpoint

model_router = APIRouter(prefix="/api/v1/model", tags=["model"])
model_router.include_router(auto_endpoint.router)
model_router.include_router(google_endpoint.router)
model_router.include_router(alibaba_endpoint.router)
model_router.include_router(mistral_endpoint.router)
model_router.include_router(meta_endpoint.router)
