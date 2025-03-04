from fastapi import APIRouter

import routes.endpoint as routes

api_router = APIRouter()
api_router.include_router(routes.endpoint)
