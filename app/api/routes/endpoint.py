from fastapi import APIRouter
from app.api.routes.model.google import endpoint

model_router = APIRouter(prefix="/api/v1/model", tags=["model"])
model_router.include_router(endpoint.google_router)
