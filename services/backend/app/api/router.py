from fastapi import APIRouter
from app.api.routes.samples import router as samples_router

api_router = APIRouter()
api_router.include_router(samples_router, tags=["samples"])
